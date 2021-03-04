
FROM python:3-alpine as base

FROM base as builder

RUN mkdir /install

WORKDIR /install

RUN pip install --prefix=/install tornado

FROM base

COPY --from=builder /install /usr/local

COPY . /app

WORKDIR /app

# Make port 80 available to the world outside this container
EXPOSE 80

CMD ["python", "-m", "chat.main", "--port=80"]
