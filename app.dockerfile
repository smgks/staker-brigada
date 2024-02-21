FROM python:3.11

WORKDIR /data

COPY ./requirements.txt /data/requirements.txt

RUN pip install --no-cache-dir -r /data/requirements.txt

EXPOSE 80

COPY ./app /data/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
