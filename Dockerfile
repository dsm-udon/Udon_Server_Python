FROM bitnami/python:3.9

COPY . /src

WORKDIR /src

ENV PYTHONUNBUFFERED 1

ENV SERVER_PORT 8000

ENV SERVER_HOST 127.0.0.1

EXPOSE 8000

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["python", "-m", "uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]