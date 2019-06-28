FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /django_code_polls
WORKDIR /django_code_polls
COPY requirements.txt /django_code_polls/
RUN pip install -r requirements.txt
COPY . /django_code_polls/
