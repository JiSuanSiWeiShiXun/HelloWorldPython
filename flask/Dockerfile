FROM python:3.8.18 AS base

FROM base
WORKDIR /home/ruler
ADD . .
ENTRYPOINT ["python","app.py"]