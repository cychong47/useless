FROM python:3
LABEL description="Dockerize pyftplib based ftp server"
LABEL maintainer="Chaeyong Chong <cychong@gmail.com>"

RUN pip3 install pyftpdlib
RUN pip3 install pyYAML

ENV PYFTPD_INCOMING_DIR /tmp
ENV PYFTPD_DOC_DDIR /tmp
ENV PYFTPD_LOG_DDIR /tmp

RUN git clone https://github.com/cychong47/useless.git
CMD ["/usr/local/bin/python3", "./useless/pyftpd.py"]

#COPY pyftpd.py .
#CMD ["/usr/local/bin/python3", "./pyftpd.py"]
