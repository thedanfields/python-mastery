FROM python:3
ARG env

RUN echo $env

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

CMD [ python ]