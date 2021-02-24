FROM python:3.8.5
LABEL MAINTAINER="Rodrigo Cunha <rodrigo.cunha@usp.br>"

RUN apt-get update && \
apt-get upgrade -y

RUN apt-get install bash
RUN apt-get install sudo
RUN apt-get install python3-sphinx -y

ENV G_ID=1000 \
    U_ID=1000 \
    U_NAME=user01 \
    PASS=pass

ENV PATH="/home/$U_NAME/.local/bin:${PATH}"

RUN addgroup --gid $G_ID $U_NAME
RUN adduser --uid $U_ID --ingroup $U_NAME --shell /bin/bash --disabled-password --gecos "" $U_NAME
RUN usermod -aG 100 $U_NAME
RUN usermod -aG sudo $U_NAME
RUN echo "$U_NAME:$PASS" | chpasswd
RUN /usr/local/bin/python -m pip install --upgrade pip

USER $U_NAME
WORKDIR /usr/src/config/

ADD requirements.txt /usr/src/config/
ADD setup.py /usr/src/config/
RUN pip install -r /usr/src/config/requirements.txt --no-warn-script-location
RUN python /usr/src/config/setup.py

WORKDIR /usr/src/code/

RUN kedro install --build-reqs

EXPOSE 8888
EXPOSE 4141
EXPOSE 5000
