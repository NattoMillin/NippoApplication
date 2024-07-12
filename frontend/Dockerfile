FROM node:20.13.1-slim

WORKDIR /home/node/dev

RUN apt-get update && apt-get install -y sudo && \
    echo "node ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN npm install -g npm@latest \ 
    && chown -R node:node /home/node/dev
USER node

