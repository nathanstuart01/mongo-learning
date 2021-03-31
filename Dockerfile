FROM mongo:latest

VOLUME ["/data/db"]

WORKDIR /data

ENV MONGO_INITDB_ROOT_USERNAME=root
ENV MONGO_INITDB_ROOT_PASSWORD=password 

EXPOSE 27017

CMD ["mongod"]


