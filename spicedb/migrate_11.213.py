# coding=utf-8
'''
@File    :   migrate_11.213.py
@Time    :   2024/01/19 19:07:43
@Author  :   youling 
@Contact :   xiezhihong@kingsoft.com
@Desc    :   迁移某个spiceDB的所有关系，用emai代替uid
1. 导出schema
2. 【备份】导出spicedb的所有关系
3. 【刷新spiceDB】导出所有关系并替换uid，写入spicedb
4. 停服snake-web
5. 【snake-web】更新snake-web将网关传入的email视为uid
6. 【mongodb】备份user表，更新数据库中的uid
7. 启动snake-web
'''
import datetime
import pathlib
import re
from typing import List

from spicedb import SpiceDBClient, str_2_relationship, \
    licObjectType, licPermission, licRelation, licSingletonID
from migrate import bulk_export_relationship

import pymongo
from authzed.api.v1 import (
    Client,
    Relationship, ObjectReference, SubjectReference,
    BulkExportRelationshipsRequest, BulkExportRelationshipsResponse,
    BulkImportRelationshipsRequest, BulkImportRelationshipsResponse,
    Consistency,
)
from authzed.api.v1.core_pb2 import Cursor

DATABASE = "project1"
COLLECTION = "user"

mongo_client: pymongo.MongoClient = None


def get_mongo_client() -> pymongo.MongoClient:
    global mongo_client
    if mongo_client is None:
        mongo_client = pymongo.MongoClient(host="10.11.11.213")
    return mongo_client

def get_new_uid(email: str) -> str:
    return email.replace("@", "--").replace(".", "-")

def get_email(uid: str) -> str|None:
    ret: dict = get_mongo_client().get_database(DATABASE).get_collection(COLLECTION).find_one({"_id": uid})
    if not ret:
        raise Exception("user not exist [uid]%s" % uid)
    if "email" in ret:
        return ret["email"]

def export_relationship_and_refresh_uid(client: Client, export_path: str|None = None):
    count = 0    # relationship总数
    token = None # 这个token是个字符串，不太理解实际代表什么；但是它可以决定返回的起始位置
    relationship_set = set()
    req = BulkExportRelationshipsRequest(
        consistency=Consistency(fully_consistent=True),
        optional_cursor=Cursor(token=token) if token else None,
    )
    resp = client.BulkExportRelationships(request=req)

    for item in resp:
        item: BulkExportRelationshipsResponse
        print(item.after_result_cursor)
        for r in item.relationships:
            count += 1

            resource_type = r.resource.object_type
            resource_id = r.resource.object_id
            relation = r.relation
            subject_type = r.subject.object.object_type
            subject_id = r.subject.object.object_id
            
            if subject_type == "user" and subject_id != "*":
                email: str = get_email(subject_id)
                subject_id = get_new_uid(email)

            relationship = f"{resource_type}:{resource_id}#{relation}@{subject_type}:{subject_id}"

            if relationship in relationship_set:
                print("duplicate relationship: %s" % relationship) # 不应该出现的情况，重复导出关系
            else:
                relationship_set.add(relationship)
        token = item.after_result_cursor.token

    if export_path:
        with open(export_path, "w") as f:
            for r in relationship_set:
                f.write(r + "\n")
    
    print(count)
    return relationship_set.pop()

def import_relationship_from_file(client: SpiceDBClient, path: str):
    with open(path, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            r = str_2_relationship(line)
            resource_type = licObjectType(r.resource.object_type)
            resource_id = r.resource.object_id
            relation = licRelation(r.relation)
            subject_type = licObjectType(r.subject.object.object_type)
            subject_id = r.subject.object.object_id
            
            client.write_relationship(
                subject_type=subject_type,
                subject_id=subject_id,
                relation=relation,
                resource_type=resource_type,
                resource_id=resource_id
            )

def refresh_user_id(mongo_client: pymongo.MongoClient):
    """将user表中的uid更新为邮箱"""
    db = mongo_client[DATABASE]  # Replace with your database name
    users = db[COLLECTION]  # Replace with your users collection name

    user_count = 0
    for user in users.find():
        if "email" not in user:
            continue
        user_count += 1
        new_uid = get_new_uid(user["email"])
        print(user["email"], user["_id"], new_uid)

        # Create a new document with the new uid
        new_user = dict(user)
        new_user['_id'] = new_uid

        # Delete the old document and insert the new one
        users.delete_one({'_id': user['_id']})
        users.insert_one(new_user)
    print(user_count)


if __name__ == "__main__":
    refresh_user_id(get_mongo_client())

    # date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # bak_name = f"./migrate/relationships-{date}.zed"
    # file_name = f"./migrate/relationships-new-{date}.zed"

    # c = SpiceDBClient()
    # schema_path = c.read_schema()
    # bulk_export_relationship(c.client, bak_name)
    # export_relationship_and_refresh_uid(c.client, file_name)

    # # c = SpiceDBClient(endpoint="10.11.89.55:50051", token="foobar")
    # # c.read_schema()
    # # c.init_schema(schema_path)
    # import_relationship_from_file(c, file_name)
    # check_file_name = f"./migrate/89.55-{date}.zed"
    # bulk_export_relationship(c.client, check_file_name)
    # # 检查89.55的关系是否和213一致
    # r_213 = set()
    # r_55 = set()
    # with open(file_name, "r") as f213:
    #     lines = f213.readlines()
    #     for line in lines:
    #         r_213.add(line)
    
    # with open(check_file_name, "r") as f55:
    #     lines = f55.readlines()
    #     for line in lines:
    #         r_55.add(line)
    # print(f"【数据一致性检查】{r_213==r_55}")
    