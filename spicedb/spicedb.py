from authzed.api.v1 import (
    Client,
    ObjectReference,
    Relationship,
    RelationshipUpdate,
    SubjectReference,
    WriteRelationshipsRequest,
    WriteSchemaRequest,
    CheckPermissionRequest,
    CheckPermissionResponse,
)
from grpcutil import insecure_bearer_token_credentials, bearer_token_credentials

client = Client(
    "172.17.0.4:50051", 
    insecure_bearer_token_credentials("kingsoft")
)

def init_schema():
    SCHEMA = """
    definition user {}

    definition system {
        relation superuser: user
        relation normal_project: project
    }

    definition project {
        relation admin: user | system#superuser
        relation editor: user
        relation executor: user
        relation viewer: user
        relation normal_resource: resource
        permission create = admin + editor
        permission edit = admin + editor
        permission execute = admin + editor + executor
        permission share = admin + editor + executor + viewer
        permission view = admin + editor + executor + viewer
    }

    definition resource {
        relation admin: user | project#admin
        relation editor: user | project#editor
        relation executor: user | project#executor
        relation viewer: user | project#viewer
        permission create = admin + editor
        permission edit = admin + editor
        permission execute = admin + editor + executor
        permission share = admin + editor + executor + viewer
        permission view = admin + editor + executor + viewer
    }
    """

    resp = client.WriteSchema(WriteSchemaRequest(schema=SCHEMA))
    print("ok")

def create_project(project_id):
    r = RelationshipUpdate(
        operation=RelationshipUpdate.Operation.OPERATION_CREATE,
        relationship=Relationship(
            resource=ObjectReference(object_type="system", object_id="system_root"),
            relation="normal_project",
            subject=SubjectReference(
                object=ObjectReference(
                    object_type="project",
                    object_id=project_id
                )
            )
        )
    )
    client.WriteRelationships(WriteRelationshipsRequest(updates=[r]))
    print("ok")

def create_super_user(user_id):
    r = RelationshipUpdate(
        operation=RelationshipUpdate.Operation.OPERATION_CREATE,
        relationship=Relationship(
            resource=ObjectReference(object_type="system", object_id="system_root"),
            relation="superuser",
            subject=SubjectReference(
                object=ObjectReference(
                    object_type="user",
                    object_id=user_id
                )
            )
        )
    )
    client.WriteRelationships(WriteRelationshipsRequest(updates=[r]))
    print("ok")

def assign_project_member(project_id, user_id, member_type):
    r = RelationshipUpdate(
        operation=RelationshipUpdate.Operation.OPERATION_CREATE,
        relationship=Relationship(
            resource=ObjectReference(object_type="project", object_id=project_id),
            relation=member_type,
            subject=SubjectReference(
                object=ObjectReference(
                    object_type="user",
                    object_id=user_id
                )
            )
        )
    )
    client.WriteRelationships(WriteRelationshipsRequest(updates=[r]))
    print("ok")

def create_project_resource(project_id, resource_id):
    r = RelationshipUpdate(
        operation=RelationshipUpdate.Operation.OPERATION_CREATE,
        relationship=Relationship(
            resource=ObjectReference(object_type="project", object_id=project_id),
            relation="normal_resource",
            subject=SubjectReference(
                object=ObjectReference(
                    object_type="resource",
                    object_id=resource_id
                )
            )
        )
    )
    client.WriteRelationships(WriteRelationshipsRequest(updates=[r]))
    print("ok")

def assign_resource_member(resource_id, user_id, member_type):
    r = RelationshipUpdate(
        operation=RelationshipUpdate.Operation.OPERATION_CREATE,
        relationship=Relationship(
            resource=ObjectReference(object_type="resource", object_id=resource_id),
            relation=member_type,
            subject=SubjectReference(
                object=ObjectReference(
                    object_type="user",
                    object_id=user_id
                )
            )
        )
    )
    client.WriteRelationships(WriteRelationshipsRequest(updates=[r]))
    print("ok")

def check_resource_permission(resource_id, user_id, permission):
    resource = ObjectReference(object_type="resource", object_id=resource_id)
    user = SubjectReference(object=ObjectReference(object_type="user", object_id=user_id))
    resp = client.CheckPermission(CheckPermissionRequest(
        resource=resource,
        subject=user,
        permission=permission
    ))
    return resp.permissionship == CheckPermissionResponse.PERMISSIONSHIP_HAS_PERMISSION

# # 初始化
# init_schema()

# # 添加项目 project_a, project_b
# create_project("project_a")
# create_project("project_b")

# # 添加超级管理员 user_super
# create_super_user("user_super")

# # 添加项目管理员
# assign_project_member("project_a", "admin_project_a", "admin")
# assign_project_member("project_b", "admin_project_b", "admin")

# # 添加项目查看者
# assign_project_member("project_a", "viewer_project_a", "viewer")
# assign_project_member("project_b", "viewer_project_b", "viewer")

# # 添加资源
# create_project_resource("project_a", "resource_a_pj_a")
# create_project_resource("project_a", "resource_b_pj_a")
# create_project_resource("project_b", "resource_a_pj_b")
# create_project_resource("project_b", "resource_b_pj_b")

# # 添加资源管理员
# assign_resource_member("resource_a_pj_a", "admin_resource_a_pj_a", "admin")
# assign_resource_member("resource_a_pj_b", "admin_resource_a_pj_b", "admin")

# # 添加资源查看者
# assign_resource_member("resource_a_pj_a", "viewer_resource_a_pj_a", "viewer")
# assign_resource_member("resource_a_pj_b", "viewer_resource_a_pj_b", "viewer")

#-------------------验证
def check_permission_debug(resource_id, user_id, action):
    print(f"{user_id} {action} permission for {resource_id}: {check_resource_permission(resource_id, user_id, action)} \n")

# 超级用户对任何资源都有访问权限
check_permission_debug("resource_a_pj_a", "user_super", "edit")
check_permission_debug("resource_b_pj_b", "user_super", "edit")

# 项目用户对项目下的资源拥有同等访问权限
check_permission_debug("resource_a_pj_a", "admin_project_a", "edit")
check_permission_debug("resource_a_pj_b", "admin_project_a", "edit")

# 资源用户仅能访问本资源
check_permission_debug("resource_a_pj_a", "admin_resource_a_pj_a", "edit")
check_permission_debug("resource_b_pj_a", "admin_resource_a_pj_a", "admin")
