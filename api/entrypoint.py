#!/usr/bin/env python3
import json
import MySQLdb
import re
import secrets
import ssl
import string
import sys
import tornado.httpserver
import tornado.ioloop
import tornado.web
import traceback

db_connection = MySQLdb.connect(
  host="db.mqtt.bavartec.de",
  port=3306,
  user="bavartec",
  passwd="cetravab",
  db="vernemq_db"
)
print("connected")

class Cursor():
  def __enter__(self):
    db_connection.ping(True)
    self.cursor = db_connection.cursor()
    return self.cursor

  def __exit__(self, *args):
    self.cursor.close()
    db_connection.commit()

def status(code):
  return tornado.web.HTTPError(code)

class BaseHandler(tornado.web.RequestHandler):
  def post(self):
    try:
      self.postUnsafe()
    except tornado.web.HTTPError:
      raise
    except:
      print(self.json_args)
      traceback.print_exception(*sys.exc_info())
      raise
    finally:
      sys.stdout.flush()

  def prepare(self):
    self.json_args = dict()

    if not self.request.headers.get("Content-Type", "").startswith("application/json"):
      raise status(400)

    try:
      self.json_args = json.loads(self.request.body)
    except:
      raise status(400)

class RegisterHandler(BaseHandler):
  def postUnsafe(self):
    user = self.json_args.get("user")
    password = self.json_args.get("pass")

    if type(user) != str or type(password) != str:
        raise status(400);

    if re.fullmatch("[A-Za-z][A-Za-z0-9-_]{6,30}[A-Za-z0-9]", user) is None:
      self.write("username-invalid")
      return

    if re.fullmatch("([A-Za-z0-9]|" + '|'.join(map(re.escape, string.punctuation)) + '){8,32}', password) is None:
      self.write("password-invalid")
      return

    with Cursor() as cursor:
      cursor.execute("""SELECT password, UNHEX(SHA2(CONCAT(%s, salt), 256))
                        FROM vmq_auth_acl
                        WHERE username = %s""",
                        (password, user))
      existing = cursor.fetchone()

    if existing is not None:
      if existing[0] == existing[1]:
        self.write("success")
        return
      else:
        self.write("username-conflict")
        return

    salt = "".join(secrets.choice(string.digits + string.ascii_letters + string.punctuation) for _ in range(32))

    with Cursor() as cursor:
      cursor.execute("""INSERT INTO vmq_auth_acl (username, password, salt)
                        VALUES (%s, UNHEX(SHA2(CONCAT(%s, %s), 256)), %s)""",
                        (user, password, salt, salt))

    self.write("success")

class UnregisterHandler(BaseHandler):
  def postUnsafe(self):
    user = self.json_args.get("user")
    password = self.json_args.get("pass")

    if type(user) != str or type(password) != str:
        raise status(400);

    with Cursor() as cursor:
      cursor.execute("""SELECT password, UNHEX(SHA2(CONCAT(%s, salt), 256))
                        FROM vmq_auth_acl
                        WHERE username = %s""",
                        (password, user))
      existing = cursor.fetchone()

    if existing is None:
      self.write("unknown-username")
      return

    if existing[0] != existing[1]:
      self.write("wrong-password")
      return

    with Cursor() as cursor:
      cursor.execute("""DELETE FROM vmq_auth_acl
                        WHERE username = %s""",
                        (user,))

    self.write("success")

def make_app():
  return tornado.web.Application([
    (r"/register", RegisterHandler),
    (r"/unregister", UnregisterHandler),
  ])

if __name__ == "__main__":
  server = tornado.httpserver.HTTPServer(make_app(), ssl_options={
    "certfile": "/etc/letsencrypt/live/api.mqtt.bavartec.de/fullchain.pem",
    "keyfile": "/etc/letsencrypt/live/api.mqtt.bavartec.de/privkey.pem",
  })
  server.listen(443)
  print("online")
  tornado.ioloop.IOLoop.instance().start()
