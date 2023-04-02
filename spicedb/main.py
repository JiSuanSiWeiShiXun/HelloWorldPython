# coding=utf-8
from authzed.api.v1 import (
    Client,
    ObjectReference,
    Relationship,
    RelationshipUpdate,
    SubjectReference,
    WriteRelationshipsRequest,
    WriteSchemaRequest,
    ReadSchemaRequest,
    LookupResourcesRequest
)
from grpcutil import insecure_bearer_token_credentials

client = Client(
    "localhost:50051",
    insecure_bearer_token_credentials("somerandomkeyhere"),
    # For SpiceDB behind TLS, use:
    # bearer_token_credentials("kingsoft"),
)

def init_schema():
    """
    创建/覆盖重写schema
    """
    with open("collection.zed", encoding="utf-8") as schema_file:
        client.WriteSchema(WriteSchemaRequest(schema=schema_file.read()))
        print("ok")


def read_schema():
    """
    查询schema
    """
    schema_text = client.ReadSchema(ReadSchemaRequest())
    print("xxx", schema_text)

def add_relationship(*,
                     subject_type: str,
                     subject_id: str,
                     relation: str,
                     resource_type: str,
                     resource_id: str,
                     ) -> str:
    """
    add relationship
    """
    relationship = Relationship(
        resource=ObjectReference(object_type=resource_type,
                                 object_id=resource_id),
        relation=relation,
        subject=SubjectReference(object=ObjectReference(
            object_type=subject_type,
            object_id=subject_id
        ))
    )
    resp = client.WriteRelationships(
        WriteRelationshipsRequest(
            updates=[
                RelationshipUpdate(
                    operation=RelationshipUpdate.Operation.OPERATION_CREATE,
                    relationship=relationship
                )
            ]
        )
    )
    print("create success", resp.written_at.token)
    return resp.written_at.token

def remove_relationship(*,
                     subject_type: str,
                     subject_id: str,
                     relation: str,
                     resource_type: str,
                     resource_id: str,
                     ) -> str:
    """
    remove relationship
    """
    relationship = Relationship(
        resource=ObjectReference(object_type=resource_type,
                                 object_id=resource_id),
        relation=relation,
        subject=SubjectReference(object=ObjectReference(
            object_type=subject_type,
            object_id=subject_id
        ))
    )
    resp = client.WriteRelationships(
        WriteRelationshipsRequest(
            updates=[
                RelationshipUpdate(
                    operation=RelationshipUpdate.Operation.OPERATION_DELETE,
                    relationship=relationship
                )
            ]
        )
    )
    print("delete success", resp.written_at.token)
    return resp.written_at.token


# [查] 查询object实例：（查询某人有哪些物品？某物品的主人是谁？查询某）LookupResources
# [CheckPermission]查询是否有操作权限？
# [查] 查询resources
def lookup_resources(*,
                     resource_type: str,
                     permission: str, # ???
                     ):
    """
    look up resources
    """
    req = LookupResourcesRequest(
        resource_object_type=resource_type,
        permission=permission,
        subject=SubjectReference(object=ObjectReference(
                object_id="",
                object_type=""
            )
        )
    )
    client.LookupResources(request=req)

# 【改schema】
# 1. 增、删、改：object｜relation｜permission
# 2. 查询schema


# # [增] 增加object实例：用户、物品（增加物品同时也会增加relation
# add_relationship(
#     subject_type="user",
#     subject_id="xiezhh",
#     relation="owner",
#     resource_type="object",
#     resource_id="licha"
# )

# # [删] 删除relationship
# remove_relationship(
#     subject_type="user",
#     subject_id="xiezhh",
#     relation="owner",
#     resource_type="object",
#     resource_id="licha"
# )

