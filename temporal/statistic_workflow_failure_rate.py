# import grpc
# from temporalio.api.enums.v1 import WorkflowExecutionStatus
# from temporalio.api.workflowservice.v1 import ListWorkflowExecutionsRequest, WorkflowServiceStub

# channel = grpc.insecure_channel("10.11.68.34:7233")
# service = WorkflowServiceStub(channel)

# # 定义 workflow 的类型
# workflow_type = "StatisticWorkflow"

# # 创建一个请求以列出指定类型的所有 workflow
# request = ListWorkflowExecutionsRequest()
# request.namespace = "default"
# request.query = f"WorkflowType = '{workflow_type}'"

# try:
#     response = service.ListWorkflowExecutions(request)
#     total_statistic_workflows = len(response.executions)

#     failed_statistic_workflows = 0
#     for workflow in response.executions:
#         if workflow.status == int(WorkflowExecutionStatus.WORKFLOW_EXECUTION_STATUS_FAILED):
#             failed_statistic_workflows += 1

#     failure_rate = failed_statistic_workflows / total_statistic_workflows

#     print(f"Total StatisticWorkflow workflows: {total_statistic_workflows}")
#     print(f"Failed StatisticWorkflow workflows: {failed_statistic_workflows}")
#     print(f"Failure rate: {failure_rate}")
# except grpc.RpcError as e:
#     print(f"An error occurred: {e}")

import grpc
from datetime import datetime
from google.protobuf.json_format import MessageToDict
from temporalio.api.workflowservice.v1 import ListWorkflowExecutionsRequest, WorkflowServiceStub

channel = grpc.insecure_channel("10.11.89.55:7233")
service = WorkflowServiceStub(channel)

# 定义 workflow 的类型
workflow_type = "StatisticWorkflow"

# 创建一个请求以列出指定类型的所有 workflow
request = ListWorkflowExecutionsRequest()
request.namespace = "default"
request.query = f"WorkflowType = '{workflow_type}'"

try:
    response = service.ListWorkflowExecutions(request)
    # total_statistic_workflows = len(response.executions)

    today_failed_statistic_workflows = 0
    today_total_statistic_workflows = 0
    d = MessageToDict(response)

    today = datetime.now().date()

    for execution in d['executions']:
        execution_date = datetime.strptime(execution["executionTime"], "%Y-%m-%dT%H:%M:%S.%fZ").date()
        if execution_date == today:
            today_total_statistic_workflows += 1

    for execution in d["executions"]:
        execution_date = datetime.strptime(execution["executionTime"], "%Y-%m-%dT%H:%M:%S.%fZ").date()
        if execution["status"] == "WORKFLOW_EXECUTION_STATUS_FAILED" and execution_date == today:
            today_failed_statistic_workflows += 1

    failure_rate = today_failed_statistic_workflows / today_total_statistic_workflows
    failure_rate = round(failure_rate, 4)

    print(f"Total StatisticWorkflow workflows: {today_total_statistic_workflows}")
    print(f"Failed StatisticWorkflow workflows: {today_failed_statistic_workflows}")
    print(f"Failure rate: {failure_rate}")
except grpc.RpcError as e:
    print(f"An error occurred: {e}")
