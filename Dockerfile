FROM ubuntu
MAINTAINER Łukasz Wieczorek <luke@soiree.tech>
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -y && apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    fish \
 && rm -rf /var/lib/apt/lists/*
COPY . /app/
WORKDIR /app/
RUN ./install.fish
CMD ./run_prod.fish
