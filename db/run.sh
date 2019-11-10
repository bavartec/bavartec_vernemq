set -e

docker build -t db .
docker run -t -i \
  -v "/var/lib/mysql:/var/lib/mysql" \
  -p 3306:3306 \
  --env-file=env \
  --name db db
