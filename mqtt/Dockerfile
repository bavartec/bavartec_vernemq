FROM erlio/docker-vernemq:1.9.2-1

USER vernemq

COPY --chown=vernemq:vernemq vernemq.conf /vernemq/etc/vernemq.conf
COPY --chown=vernemq:vernemq mysql.lua /vernemq/share/lua/auth/mysql.lua

EXPOSE 8883/tcp

CMD ["start_vernemq"]
