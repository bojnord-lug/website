FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /lug-website
WORKDIR /lug-website
COPY requirements.txt /lug-website/
RUN pip install -r requirements.txt
COPY . /lug-website/