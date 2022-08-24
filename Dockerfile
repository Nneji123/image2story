FROM python:3.8.13-slim-bullseye

WORKDIR /app

RUN apt-get -y update  && apt-get install -y \
  python3-dev \
  apt-utils \
  python-dev \
  git \
  build-essential \
&& rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade setuptools 

COPY . .

RUN pip install -r requirements.txt

RUN python download.py

# EXPOSE 8000:8000

# CMD uvicorn app:app --reload --host 0.0.0.0 --port 8000

#CMD uvicorn app:app --host=0.0.0.0 --port=${PORT:-5000}

CMD gunicorn -w 2 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:$PORT