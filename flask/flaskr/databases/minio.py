# coding=utf-8
from minio import Minio
from minio.error import S3Error

client = Minio(
    endpoint="10.11.81.87:9000",
    access_key='QJUH6A2CQN2C6HO6W0DJ',
    secret_key='T8Nj78egoxvYTYig+Ufa9sUPQyg1K5fOwbLuamqM',
)

found = client.bucket_exists()