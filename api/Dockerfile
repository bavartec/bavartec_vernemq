FROM ubuntu

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-mysqldb
RUN pip3 install tornado

COPY entrypoint.py /entrypoint.py

EXPOSE 443/tcp

CMD ["/entrypoint.py"]
