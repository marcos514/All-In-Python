# FROM python:3.9.7
# RUN mkdir /app/
# COPY . /app/api
# RUN pip install --upgrade pip && pip install -r /app/api/requirements.txt
# WORKDIR /app/api
# CMD ["supervisord", "-n", "-c","/app/api/supervisor/supervisord.conf"]

FROM python:3.9

WORKDIR /backend

COPY ./api/requirements.txt /backend/requirements.txt

RUN pip install --progress-bar off --no-cache-dir --upgrade -r /backend/requirements.txt

COPY ./api/app /backend/app
COPY ./common /backend/common

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
