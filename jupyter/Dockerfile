FROM python:3.6

RUN apt update
RUN pip install --upgrade pip

COPY requirements.txt /home
RUN pip install --no-cache-dir -r /home/requirements.txt

COPY start_jupyter.sh /home

WORKDIR /home

EXPOSE 8000