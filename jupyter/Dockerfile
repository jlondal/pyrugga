FROM python:3.6

RUN apt update
RUN pip install --upgrade pip

COPY requirements.txt /home
RUN pip install --no-cache-dir -r /home/requirements.txt

COPY start_jupyter.sh /home

COPY 719101_wspvnat_new.xml /home
COPY 918053_walvfra_new.xml /home

WORKDIR /home

EXPOSE 8000
