FROM conda/miniconda3

ADD . /app

WORKDIR /app

# RUN apt-get update &&  apt-get -y upgrade
# RUN apt-get -y install build-essential
RUN apt-get update && \
    apt-get -y install git gcc g++ sox libsox-dev libsox-fmt-all

RUN pip install --upgrade --no-cache-dir pip \
    && pip install --no-cache-dir -r requirements.txt

RUN apt-get clean

RUN apt-get autoremove -y

# RUN rm -rf /var/cache/apk/*