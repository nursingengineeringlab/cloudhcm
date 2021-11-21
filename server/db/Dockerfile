FROM postgres:10.11-alpine
#COPY init-user-db.sh /docker-entrypoint-initdb.d/
#COPY init.sql /docker-entrypoint-initdb.d/
ENV POSTGRES_USER CHSUser1
ENV POSTGRES_PASSWORD A9EQFT6gS#LRHHwo75MRPZQl8mWaA02N&
ENV POSTGRES_DB SensorData
COPY init.sql /docker-entrypoint-initdb.d/

