FROM python:3.12-alpine

WORKDIR /app

COPY requirements-prod.txt .
RUN pip install -r requirements-prod.txt
COPY app ./app

EXPOSE 8000

ENTRYPOINT [ "fastapi" ]
CMD [ "run", "app" ]
