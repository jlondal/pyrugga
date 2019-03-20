FROM python:3.6

RUN pip install --upgrade pip
RUN apt update

RUN git clone --recursive https://github.com/dmlc/xgboost
RUN cd xgboost; make -j4
RUN apt update

RUN apt-get install zip unzip -y
RUN apt-get install libhdf5-serial-dev -y

COPY requirements.txt /home
RUN pip install --no-cache-dir -r /home/requirements.txt

COPY start_jupyter.sh /home

WORKDIR /home

EXPOSE 8000
