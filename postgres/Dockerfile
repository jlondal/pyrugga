FROM postgres:alpine
EXPOSE 5434
RUN mkdir -p /tmp/psql_data
COPY setup.sql /docker-entrypoint-initdb.d/
