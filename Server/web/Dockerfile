FROM node:latest

WORKDIR /code
ENV PATH /code/care_app/node_modules/.bin:$PATH
#COPY package.json ./
#ADD package.json /code/package.json
COPY . /code/

# RUN yarn add @fortawesome/free-solid-svg-icons
# RUN yarn add @fortawesome/react-fontawesome
# RUN yarn add @ant-design/compatible
#RUN yarn @fortawesome/fontawesome-svg-core
RUN npm install react
RUN npm install -g npm@7.5.3 --silent
# RUN npm install -g npm --silent
RUN npm install socket.io-client
RUN npm install -g react-scripts

RUN cd /code/care_app/; yarn install
