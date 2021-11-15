FROM node:latest
WORKDIR /code
COPY . /code/

RUN npm install -g npm@7.5.3 --silent
RUN npm install --quiet
RUN npm install zeromq
RUN npm install ip
RUN npm install socket.io@4.0.0
RUN npm install dotenv

EXPOSE 4000