FROM python:3.8.6

RUN pip install --upgrade pip

WORKDIR /foodgram
RUN mkdir /foodgram/static
RUN mkdir /foodgram/media

COPY . .

RUN pip install -r requirements.txt

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000