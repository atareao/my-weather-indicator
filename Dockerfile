FROM ubuntu


RUN apt-get update -y && \
    apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y build-essential \
                      binutils \
                      lintian \
                      debhelper \
                      dh-make \
                      gnupg2 \
                      devscripts

WORKDIR /app
CMD ["/bin/bash", "/app/mybuilder.sh"]
