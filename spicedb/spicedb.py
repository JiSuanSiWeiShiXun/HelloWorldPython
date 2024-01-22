# coding=utf-8
import logging
import re
from enum import Enum
from typing import Union, List

from authzed.api.v1 import (
    Client,
    ObjectReference,
    Relationship,
    RelationshipUpdate,
    SubjectReference,
    RelationshipFilter, SubjectFilter,
    WriteRelationshipsRequest, WriteSchemaRequest,
    DeleteRelationshipsRequest, DeleteRelationshipsResponse, 
    ReadRelationshipsRequest, ReadRelationshipsResponse,
    ReadSchemaRequest, ReadSchemaResponse, 
    CheckPermissionRequest, CheckPermissionResponse,
    LookupResourcesRequest, LookupResourcesResponse,
    LookupSubjectsRequest, LookupSubjectsResponse,
    Consistency
)
from grpcutil import (
    bearer_token_credentials,
    insecure_bearer_token_credentials
)
import grpc

logging.basicConfig(level=logging.DEBUG)

# with open("./ca.crt", "rb") as f:
#     ca_cert = f.read()

# client = Client(
#     # "localhost:50051",
#     "10.11.68.148:50051",
#     bearer_token_credentials("kingsoft", certChain=ca_cert),
#     # 这里有个坑，如果服务器部署在远端，必须要使用TLS协议加密
#     # 因为这个insecure_bearer_token_cretentials()的实现不支持向真实TCP地址的不安全链接发送credential，需要自己实现对每次请求都构造credential
#     # insecure_bearer_token_credentials("kingsoft"), 
# )

def init_client(crt_path: str="") -> Client:
    if not crt_path:
        crt_path = "./ca.crt"
    with open(crt_path, "rb") as f:
        ca_cert = f.read()
    
    global client
    # client = Client(
    #     "localhost:50051",
    #     insecure_bearer_token_credentials("kingsoft"),
    # )
    client = Client(
        # "8.219.5.187:50051",
        "10.11.11.213:50051",
        bearer_token_credentials("kingsoft", certChain=ca_cert),
    )
    return client

class licObjectType(Enum):
    USER = "user" # 用户
    SYSTEM = "system" # 系统，仅一个实例即snake
    APP = "application" # 项目组；对应snake中的 GameProject
    PROJECT = "project" # 案例; 对应snake中的 Project
    LABEL = "label" # 压力机

class licRelation(Enum):
    # 对于同一个维度，枚举值定义的先后顺序是有意义的，被用于判断角色权限的大小，先定义的权限更大
    # TODO(youling): 把他们按照维度归类，提供方法判断两个角色的权限大小
    SYSTEM_ADMIN = "admin" # system's admin

    APP_MANAGER = "manager" # 项目管理者，创建项目的人自动成为
    APP_MEMBER = "member" # 项目成员
    APP_TOURIST = "tourist" # 访客
    APP_BELONG_TO = "belong_to" # 项目所属的系统，便于反查有多少项目，目前都归属于lic-system

    PROJECT_PARENT = "parent" # 案例归属的项目

    LABEL_PARENT = "parent" # 发压机归属的系统
    LABEL_AUTHORIZED_USER = "authorized_user" # 拥有发压机使用权限的人

    @classmethod
    def compare_roles(cls, role1, role2) -> bool:
        """返回role1权限是否大于role2权限
        @return True:role1>=role2 False:role1<role2 
        TODO(youling): 非不同维度不能比较
        """
        if not isinstance(role1, cls) or not isinstance(role2, cls):
            raise Exception("非Relation，类型不能比较")
        role1_index = list(cls.__members__.values()).index(role1)
        role2_index = list(cls.__members__.values()).index(role2)
        if role1_index <= role2_index:
            return True
        elif role1_index > role2_index:
            return False
    
class licPermission(Enum):
    """
    checkPermission时指定，一般用于查询当前用户是否有指定资源的xx权限
    这里就是所有权限的定义
    """
    SYSTEM_ROOT_ACCESS = "root_access" # system 超级管理员权限，可以更改人事权限

    APP_VIEW = "view" # 项目（app）的查看权限
    APP_PROJECT_EDIT = "project_edit" # 读、写、执行项目下所有案例的权限
    APP_PROJECT_VIEW = "project_view" # 查看项目下所有案例的权限

    PROJECT_EDIT = "edit" # 案例编辑权限
    PROJECT_EXECUTE = "execute" # 案例执行权限
    PROJECT_VIEW = "view" # 案例查看权限

    LABEL_EDIT = "edit"
    LABEL_ACCESS = "access"

class licSingletonID(Enum):
    """对system, project这种全局唯一实例的object_type, 这里规定了他们的object_id"""
    SYSTEM_ID = "lic-system"

# RelationshipUpdate.Operation 枚举
# WriteRelationship传入的不同操作类型
class OperationType(Enum):
	OPERATION_UNSPECIFIED = 0
	OPERATION_CREATE = 1
	OPERATION_TOUCH = 2
	OPERATION_DELETE = 3

# CheckPermissionResponse.Permissionship 枚举
# CheckPermission返回的不同结果枚举
class Permissionship(Enum):
	PERMISSIONSHIP_UNSPECIFIED = 0
	PERMISSIONSHIP_NO_PERMISSION = 1
	PERMISSIONSHIP_HAS_PERMISSION = 2
	PERMISSIONSHIP_CONDITIONAL_PERMISSION = 3

# permission_service_pb2.pyi.LookupPermissionship
# Lookup接口返回的对象中的permissionship属性
class LookupPermissionship(Enum):
	LOOKUP_PERMISSIONSHIP_UNSPECIFIED = 0
	LOOKUP_PERMISSIONSHIP_HAS_PERMISSION = 1
	LOOKUP_PERMISSIONSHIP_CONDITIONAL_PERMISSION = 2

def str_2_relationship(relationship_str: str) -> Relationship:
    tmp_list = re.split("[:@#]", relationship_str.strip())
    if len(tmp_list) != 5:
        raise Exception(f"[{relationship_str}] not recognized")
    
    print(tmp_list)
    resource_type = tmp_list[0]
    resource_id = tmp_list[1]
    relation = tmp_list[2]
    subject_type = tmp_list[3]
    subject_id = tmp_list[4]
    return Relationship(
        resource=ObjectReference(object_type=resource_type,
                                object_id=resource_id),
        relation=relation,
        subject=SubjectReference(object=ObjectReference(
            object_type=subject_type,
            object_id=subject_id
        ))
    )

class SpiceDBClient(object):
    def __init__(self, endpoint="", token="", crt_path=""):
        if not crt_path:
            crt_path = "./ca.crt"
        with open(crt_path, "rb") as f:
            ca_cert = f.read()
        
        self.endpoint = endpoint
        self.token = token
        if not endpoint:
            self.endpoint = "10.11.11.213:50051" # "8.219.5.187:50051"
        if not token:
            self.token = "kingsoft"
        
        # self.client = Client(
        #     "localhost:50051",
        #     insecure_bearer_token_credentials("kingsoft"),
        # )
        self.client = Client(
            self.endpoint,
            bearer_token_credentials(self.token, certChain=ca_cert),
        )

    def init_schema(self, path: str="permission.zed"):
        """
        创建/覆盖重写schema
        """
        with open(path, encoding="utf-8") as schema_file:
            self.client.WriteSchema(WriteSchemaRequest(schema=schema_file.read()))
            print("write schema ok!")

    def read_schema(self) -> str:
        """
        查询schema
        @return schema路径
        """
        resp: ReadSchemaResponse = self.client.ReadSchema(ReadSchemaRequest())
        print("[read schema]", resp)
        
        path = f"{self.endpoint}.zed"
        with open(path, "w") as f:
            f.write(str(resp.schema_text))
        return path

    def read_relationship(self, *,
                        resource_type: licObjectType,
                        optional_resource_id: str = "",
                        optional_relation: Union[licRelation, None] = None,
                        optional_subject_type: Union[licObjectType, None] = None,
                        optional_subject_id: str = ""
                    ) -> List[Relationship]:
        """
        [流式调用] 查询relationship
        read relationship不能用于处理permission
        """
        if optional_subject_type:
            relationship_filter = RelationshipFilter(
                resource_type=resource_type.value,
                optional_subject_filter=SubjectFilter(
                    subject_type=optional_subject_type.value,
                ),
            )
        else:
            relationship_filter = RelationshipFilter(
                resource_type=resource_type.value,
            )

        if optional_resource_id:
            relationship_filter.optional_resource_id = optional_resource_id
        if optional_relation:
            relationship_filter.optional_relation = optional_relation.value
        if optional_subject_id:
            relationship_filter.optional_subject_filter.optional_subject_id = optional_subject_id

        req = ReadRelationshipsRequest(
            relationship_filter=relationship_filter,
            consistency=Consistency(fully_consistent=True)
        )
        relationships = []
        relationships_repr = [] # relationship转化成字符串
        tokens = set() # zed token
        for resp in self.client.ReadRelationships(request=req):
            resp: ReadRelationshipsResponse
            # logging.debug("xxx%s, %s", resp, type(resp.relationship))
            relationship = {
                "resource_type": resp.relationship.resource.object_type,
                "resource_id": resp.relationship.resource.object_id,
                "relation": resp.relationship.relation,
                "subject_type": resp.relationship.subject.object.object_type,
                "subject_id": resp.relationship.subject.object.object_id,
            }
            relationships.append(relationship)
            relationships_repr.append("%s:%s#%s@%s:%s" % 
                (resp.relationship.resource.object_type, resp.relationship.resource.object_id,
                resp.relationship.relation,
                resp.relationship.subject.object.object_type, resp.relationship.subject.object.object_id))
            tokens.add(resp.read_at.token)
            
        logging.debug("[read relationship condition] [resourceType] %s [resourceID] %s [relation/permission] %s [subjectType] %s [subjectID] %s",
            resource_type, optional_resource_id, optional_relation, optional_subject_type, optional_subject_id)
        logging.info("[zedToken] %s [read relationship] success [%s]", tokens, relationships_repr)
        return relationships

    def write_relationship(self, *,
                        subject_type: licObjectType,
                        subject_id: str,
                        relation: licRelation,
                        resource_type: licObjectType,
                        resource_id: str,
                        operation_type: RelationshipUpdate.Operation.ValueType=RelationshipUpdate.Operation.OPERATION_TOUCH,
                        ) -> str:
        """
        写入 relationship
        默认使用touch而不是create, 也可以传入delete类型用于删除relationship
        """
        relationship = Relationship(
            resource=ObjectReference(object_type=resource_type.value,
                                    object_id=resource_id),
            relation=relation.value,
            subject=SubjectReference(object=ObjectReference(
                object_type=subject_type.value,
                object_id=subject_id
            ))
        )
        resp = self.client.WriteRelationships(
            WriteRelationshipsRequest(
                updates=[
                    RelationshipUpdate(
                        operation=operation_type,
                        relationship=relationship
                    )
                ]
            )
        )
        logging.info(f"[zedToken] {resp.written_at.token} [relationship] {resource_type.value}:{resource_id}#{relation.value}@{subject_type.value}:{subject_id} operate[{OperationType(operation_type).name}] write success")
        return resp.written_at.token

    def delete_relationship(self, *,
                            resource_type: licObjectType,
                            optional_resource_id: Union[str, None] = None,
                            optional_relation: Union[licRelation, None] = None,
                            optional_subject_type: Union[licObjectType, None] = None,
                            optional_subject_id: Union[str, None] = None,
                            ) -> str:
        """
        批量删除符合条件的relationship
        """
        params = {"resource_type": resource_type.value}
        if optional_resource_id:
            params["optional_resource_id"] = optional_resource_id
        if optional_relation:
            params["optional_relation"] = optional_relation.value
        if optional_subject_type:
            subject_filter_param = {"subject_type": optional_subject_type.value}
            if optional_subject_id:
                subject_filter_param["optional_subject_id"] = optional_subject_id
            params["optional_subject_filter"] = SubjectFilter(**subject_filter_param)

        req = DeleteRelationshipsRequest(
            relationship_filter=RelationshipFilter(**params)
        )
        # print(req)
        resp:DeleteRelationshipsResponse = self.client.DeleteRelationships(request=req)
        # logging.debug(resp)
        token = resp.deleted_at.token
        logging.debug("[delete relationship filter] [resourceType] %s [resourceID] %s [relation/permission] %s [subjectType] %s [subjectID] %s",
            resource_type, optional_resource_id, optional_relation, optional_subject_type, optional_subject_id)
        logging.info("[zedToken] %s [delete relationship]", token)
        return resp.deleted_at.token

    def check_permission(self, *,
                        subject_type: licObjectType,
                        subject_id: str,
                        resource_type: licObjectType,
                        resource_id: str,
                        permission: Union[licRelation, licPermission]
                        ) -> bool:
        """
        查询是否有permission/relation
        不能对wildcard关系进行check_permission查询
        @ return: 有权限返回true, 否则返回false
        """
        re = ObjectReference(
            object_type=resource_type.value,
            object_id=resource_id
        )
        sub = SubjectReference(object=ObjectReference(
            object_type=subject_type.value,
            object_id=subject_id
        ))
        req = CheckPermissionRequest(
            resource=re,
            permission=permission.value,
            subject=sub,
            consistency=Consistency(fully_consistent=True)
        )
        resp: CheckPermissionResponse = self.client.CheckPermission(req)
        logging.info("[zedToken] %s [permissionship]:%s %s:%s#%s@%s:%s ", 
            resp.checked_at.token, Permissionship(resp.permissionship).name, 
            resource_type.value, resource_id, permission.value, subject_type, subject_id)
        return resp.permissionship == Permissionship.PERMISSIONSHIP_HAS_PERMISSION.value



    def lookup_resources(self, *,
                        subject_type: licObjectType,
                        subject_id: str,
                        resource_type: licObjectType,
                        permission: Union[licRelation, licPermission]
                        )->List[str]:
        """[流式调用] 查询指定subject，指定relation/permission对应有哪些resourceID"""
        req = LookupResourcesRequest(
            resource_object_type=resource_type.value,
            permission=permission.value,
            subject=SubjectReference(object=ObjectReference(
                object_type=subject_type.value,
                object_id=subject_id,
            )),
            consistency=Consistency(fully_consistent=True),
        )
        resource_id_list = []
        zed_tokens = set()
        for resp in self.client.LookupResources(request=req):
            # logging.debug(f"[lookup resource] {resp}")
            resp: LookupResourcesResponse
            zed_tokens.add(resp.looked_up_at.token)
            if resp.permissionship == LookupPermissionship.LOOKUP_PERMISSIONSHIP_HAS_PERMISSION.value:
                resource_id_list.append(resp.resource_object_id)
        logging.info("[zedToken] %s %s:%s have [role/permission] %s over %s:%s", 
                    zed_tokens, subject_type.value, subject_id, permission.value, resource_type.value, resource_id_list)
        return resource_id_list

    def lookup_subjects(self, *,
                        resource_type: licObjectType,
                        resource_id: str,
                        subject_type: licObjectType,
                        permission: Union[licRelation, licPermission]
                        )->List[str]:
        """
        [流式调用] 查询指定relationship中的subject id有哪些
        不支持filter
        """
        req = LookupSubjectsRequest(
            permission = permission.value,
            resource = ObjectReference(
                object_type=resource_type.value,
                object_id=resource_id
                ),
            subject_object_type=subject_type.value,
            consistency=Consistency(fully_consistent=True)
        )
        subject_ids = []
        zed_tokens = set() # 因为是流式调用，我不确定返回的每个subject的zed token是不是一致的
        # 流式调用
        # print(f"hello~ client={client}") # stuck here
        for resp in self.client.LookupSubjects(request=req):
            # print(f"[lookup user] {resp}")      # this never ouput when API called in flask view functions
            resp: LookupSubjectsResponse
            zed_tokens.add(resp.looked_up_at.token)
            if resp.subject.permissionship == LookupPermissionship.LOOKUP_PERMISSIONSHIP_HAS_PERMISSION.value:
                subject_ids.append(resp.subject.subject_object_id)
        logging.info("[zedToken] %s %ss who have [%s] role/permission towards [%s:%s] are %s", 
                    zed_tokens, subject_type.value, permission.value, resource_type.value, resource_id, subject_ids)
        return subject_ids


def grant_system_admin(user_id: str):
    """
    添加(touch)系统管理员角色，角色可以代表一系列的权限
    """
    write_relationship(
        subject_type=licObjectType.USER, subject_id=user_id,
        relation=licRelation.SYSTEM_ADMIN,
        resource_type=licObjectType.SYSTEM, resource_id=licSingletonID.SYSTEM_ID.value
    )
    
def check_user_permission(self, *,
                    user_id: str,
                    resource_type: licObjectType,
                    resource_id: str,
                    permission: Union[licRelation, licPermission]
                    ) -> bool:
    """
    issues a check on whether a subject has a permission
    or is a member of a relation, on a specific resource.
    检查<user: user_id>是否有对<resource: resource_id>的权限/关系(permission)

    @ return: 有权限返回true, 否则返回false
    """
    return check_permission(
        subject_type=licObjectType.USER,
        subject_id=user_id,
        resource_type=resource_type,
        resource_id=resource_id,
        permission=permission
    )

def lookup_users_of_resource(self, *,
                resource_type: licObjectType,
                resource_id: str,
                permission: Union[licRelation, licPermission]
                )->List[str]:
    """
    [流式调用] 指定资源的relation/permission 分配给了哪些用户
    resource_type:resource_id#permission@user:uid --> 对uid进行查询
    """
    return lookup_subjects(
        resource_type=resource_type,
        resource_id=resource_id,
        subject_type=licObjectType.USER,
        permission=permission,
    )

def lookup_resources_of_user(self, *,
                    uid: str,
                    resource_type: licObjectType,
                    permission: Union[licRelation, licPermission]
                    )->List[str]:
    """
    [流式调用] 指定用户 指定permission/relationship 拥有什么资源
    resource_type:resource_id#permission@user:uid --> 对resource_id进行查询
    """
    return lookup_resources(
        subject_type=licObjectType.USER,
        subject_id=uid,
        resource_type=resource_type,
        permission=permission,
    )