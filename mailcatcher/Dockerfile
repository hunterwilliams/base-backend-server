FROM ruby:3.0
RUN apt-get update
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

RUN gem install mailcatcher

EXPOSE 1025 1080

CMD ["mailcatcher", "-f", "--ip", "0.0.0.0"]

