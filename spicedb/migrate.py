# coding=utf-8
'''
@File    :   migrate.py
@Time    :   2024/01/18 16:02:00
@Author  :   youling 
@Contact :   xiezhihong@kingsoft.com
@Desc    :   spiceDB relationship export and import
'''
import pathlib
from typing import List

from spicedb import SpiceDBClient, str_2_relationship

from authzed.api.v1 import (
    Client,
    Relationship, ObjectReference, SubjectReference,
    BulkExportRelationshipsRequest, BulkExportRelationshipsResponse,
    BulkImportRelationshipsRequest, BulkImportRelationshipsResponse,
    Consistency,
)
from authzed.api.v1.core_pb2 import Cursor

def bulk_export_relationship(client: Client, export_path: str|None = None):
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

def bulk_import_relationship(client: Client, file_path: str):
    """
    读取file_path文件中的关系，导入到spicedb中
    关系的格式： f"{resource_type}:{resource_id}#{relation}@{subject_type}:{subject_id}"
    每行一个关系
    """
    relationships: List[Relationship] = []

    path = pathlib.Path(file_path)
    if not path.exists():
        raise Exception("relationship file not found: %s" % file_path)
    with open(path.absolute(), "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            r = str_2_relationship(line)
            relationships.append(r)
    
    resp: BulkImportRelationshipsResponse = client.BulkImportRelationships(
        BulkImportRelationshipsRequest(relationships=relationships)
    )
    print(f"[num loaded] {resp.num_loaded}")


if __name__ == "__main__":
    export_file = "11.213.bak"
    import_file = "relationships.txt"

    c = SpiceDBClient()
    c.read_schema()
    tmp = bulk_export_relationship(c.client, export_path=export_file)
    str_2_relationship(tmp)
    # import_relationship(c.client, import_file)
