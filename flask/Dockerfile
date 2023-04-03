FROM python:3.10 AS base

FROM base
WORKDIR /home/ruler
ADD . .
ENTRYPOINT ["python","app.py"]