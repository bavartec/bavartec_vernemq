FROM mysql

COPY --chown=root:root auth.cnf /etc/mysql/conf.d/auth.cnf
COPY --chown=mysql:mysql ddl.sql /docker-entrypoint-initdb.d/ddl.sql

EXPOSE 3306/tcp
