FROM python:3
ARG env

RUN echo $env

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

CMD [ python ]