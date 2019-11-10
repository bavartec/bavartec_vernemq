set -e

docker build -t api .
docker run -t -i \
  -v "/etc/letsencrypt:/etc/letsencrypt" \
  -p 443:443 \
  --name api api
