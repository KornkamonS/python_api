FROM python:3.7

ADD . /app

WORKDIR /app

# RUN apt-get update &&  apt-get -y upgrade
# RUN apt-get -y install build-essential
RUN apt-get update && \
    apt-get -y install git gcc g++ sox libsox-dev libsox-fmt-all

RUN pip install --upgrade --no-cache-dir pip \
    && pip install --no-cache-dir -r requirements.txt
 
RUN pip install torch_nightly -f https://download.pytorch.org/whl/nightly/cu90/torch_nightly.html \
    && git clone https://github.com/pytorch/audio.git

WORKDIR  ./audio

RUN python setup.py install

WORKDIR  ..

RUN rm -rf audio

# RUN conda clean --all -y

RUN apt-get clean

RUN apt-get autoremove -y

# RUN rm -rf /var/cache/apk/*