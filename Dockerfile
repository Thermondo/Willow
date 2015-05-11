FROM debian:jessie
MAINTAINER Karl Hobley <karlhobley10@gmail.com>

RUN apt-get update -y
RUN apt-get install -y python python-opencv python-numpy python-pillow python-wand

VOLUME ["/src"]
WORKDIR /src
