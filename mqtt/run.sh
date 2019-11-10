set -e

docker build -t mqtt .
docker run -t -i \
  -v "/etc/letsencrypt:/etc/letsencrypt" \
  --network host \
  --name mqtt mqtt
