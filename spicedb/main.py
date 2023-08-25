# coding=utf-8
from spicedb import init_client, init_schema, \
    write_relationship, delete_relationship, check_permission, \
    lookup_resources_of_user, lookup_resources, read_relationship, \
    grant_system_admin, \
    licObjectType, licRelation, licPermission, licSingletonID


def add_app(app_key):
    write_relationship(
        resource_type=licObjectType.APP,
        resource_id=app_key,
        relation=licRelation.APP_BELONG_TO,
        subject_type=licObjectType.SYSTEM,
        subject_id=licSingletonID.SYSTEM_ID.value,
    )

def create_projects(app_key):
    """创建3000个project, 归属到指定的app下, 将app归属到全局系统下"""
    # 先删除指定app下的所有project
    delete_relationship(
        resource_type=licObjectType.PROJECT,
        optional_relation=licRelation.PROJECT_PARENT,
        optional_subject_type=licObjectType.APP,
        optional_subject_id=app_key,
    )
    write_relationship(
        resource_type=licObjectType.APP,
        resource_id=app_key,
        relation=licRelation.APP_BELONG_TO,
        subject_type=licObjectType.SYSTEM,
        subject_id=licSingletonID.SYSTEM_ID.value,
    )
    for i in range(3000):
        write_relationship(
            resource_type=licObjectType.PROJECT,
            resource_id=f"project{i+1}",
            relation=licRelation.PROJECT_PARENT,
            subject_type=licObjectType.APP,
            subject_id=app_key,
        )

def auth_glimpse(uid, project_id):
    lookup_resources_of_user(
        uid=uid,
        resource_type=licObjectType.PROJECT,
        permission=licPermission.PROJECT_VIEW
    )

    check_permission(
        resource_type=licObjectType.PROJECT, 
        resource_id=project_id,
        subject_type=licObjectType.USER, 
        subject_id=uid,
        permission=licPermission.PROJECT_VIEW
    )
    read_relationship(
        resource_type=licObjectType.PROJECT,
        optional_resource_id=project_id,
        optional_relation=licRelation.PROJECT_PARENT,
        optional_subject_type=licObjectType.APP
    )

def reparent(project_id, app_key):
    # relationships = read_relationship(
    #     resource_type=licObjectType.PROJECT,
    #     optional_resource_id=project_id,
    #     optional_relation=licRelation.PROJECT_PARENT,
    #     optional_subject_type=licObjectType.APP,
    # )
    # for r in relationships:
    #     write_relationship(
    #         resource_type=licObjectType(r["resource_type"]),
    #         resource_id=r["resource_id"],
    #         relation=licRelation(r["relation"]),
    #         subject_type=licObjectType(r["subject_type"]),
    #         subject_id=r["subject_id"],
    #         operation_type=RelationshipUpdate.Operation.OPERATION_DELETE,
    #     )
    delete_relationship(
        resource_type=licObjectType.PROJECT,
        optional_resource_id=project_id,
        optional_relation=licRelation.PROJECT_PARENT,
    ) # 一个案例同时只能属于一个项目，所以要先删除所有的父级
    write_relationship(
        subject_type=licObjectType.APP,
        subject_id=app_key,
        relation=licRelation.PROJECT_PARENT,
        resource_type=licObjectType.PROJECT,
        resource_id=project_id
    )
    
def other_check(user_id, appKey, project_id):
    lookup_resources_of_user(
        uid=user_id,
        resource_type=licObjectType.PROJECT,
        permission=licPermission.PROJECT_VIEW
    )
    check_permission(
        subject_type=licObjectType.SYSTEM,
        subject_id=licSingletonID.SYSTEM_ID.value,
        permission=licRelation.APP_BELONG_TO,
        resource_type=licObjectType.APP,
        resource_id=appKey,
    )
    check_permission(
        subject_type=licObjectType.APP,
        subject_id=appKey,
        permission=licRelation.PROJECT_PARENT,
        resource_type=licObjectType.PROJECT,
        resource_id=project_id,
    )
    check_permission(
        resource_type=licObjectType.SYSTEM, 
        resource_id=licSingletonID.SYSTEM_ID.value,
        subject_type=licObjectType.USER, 
        subject_id=user_id,
        permission=licRelation.SYSTEM_ADMIN
    )


if __name__ == "__main__":
    init_client()
    init_schema()
    former_app_key = "default"
    current_app_key = "JX3"
    project_id = "project1"
    user_id = "youling"
    # grant_system_admin(user_id)
    # create_projects(former_app_key)
    # add_app("JX3")

    lookup_resources(
        subject_type=licObjectType.APP,
        subject_id=former_app_key,
        resource_type=licObjectType.PROJECT,
        permission=licRelation.PROJECT_PARENT,
    )
    auth_glimpse(user_id, project_id)
    # print('*'*20 + " start delete " + '*'*20)
    # reparent(project_id, current_app_key)
    # print('*'*20 + " after delete " + '*'*20)
    # auth_glimpse(user_id, project_id)
