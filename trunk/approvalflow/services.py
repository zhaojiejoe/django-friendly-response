from approvalflow.models import (WorkFlow, WorkFlowInstance, WorkFlowNode,
                     WorkFlowProcess, WorkFlowInstanceStatus, WorkFlowNodeType, WorkFlowProcessStatus)
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
User = get_user_model()

class AbstractFlowService(object):
    """
    最基础的线性审批流的框架，对于复杂审批可以在此基础上扩展
    对于审批流程中的node的name可以通过某种固定方式进行数据库定义
    类似
    node: checker
    checker_audit
    checker_note
    checker 抽象审批者
    """
    name = ""

    def __init__(self):
        self.workflow = WorkFlow.objects.get(name=self.name)

    def _disable_old_workflow_instance(self, content_object):
        """
        失效旧的审批流
        """
        content_type = ContentType.objects.get_for_model(content_object)
        WorkFlowInstance.objects.filter(object_id=content_object.id, content_type=content_type,
                                                status__in=[WorkFlowInstanceStatus.INIT, WorkFlowInstanceStatus.DELIVER]
                                                ).update(status=WorkFlowInstanceStatus.STOP)

    def _gen_concrete_approver(self, approver):
        """
        获取审批者实体
        """
        kwargs = {}
        if isinstance(approver, User):
            kwargs = {"user": approver}
        return kwargs

    def _init_workflow_instance(self, content_object, applicant, approver, name):
        """
        初始化新的审批流，approver只是一个抽象审批者
        """
        workflow_instance = WorkFlowInstance.objects.create(user=applicant, workflow=self.workflow,
                                                                   content_object = content_object, status=WorkFlowInstanceStatus.DELIVER, name=name)
        init_node = WorkFlowNode.objects.get(workflow=workflow_instance.workflow, node_type=WorkFlowNodeType.START)
        workflow_process = WorkFlowProcess.objects.create(workflow_instance = workflow_instance,
                                                                        current_node = init_node, **self._gen_concrete_approver(approver))
        return workflow_process

    def _resync(self, workflow_process, note, passed):
        """
        同步审批信息回原始数据（可选）
        """
        raise NotImplementedError

    def _gen_next_approver(self, workflow_process):
        """
        生成下个节点的审批者
        """
        raise NotImplementedError

    def _gen_next_node(self, workflow_process):
        next_node = workflow_process.current_node.next_node
        if next_node is None:
            workflow_process.workflow_instance.status = WorkFlowInstanceStatus.FINISH
            workflow_process.workflow_instance.save()
        else:
            next_approver = self._gen_next_approver(workflow_process)
            if next_approver is not None:
                workflow_process = WorkFlowProcess.objects.create(workflow_instance=workflow_process.workflow_instance,
                                                                                current_node=next_node, **self._gen_concrete_approver(next_approver))
                return workflow_process
        return None

    def _approve(self, workflow_process, note, passed, writer):
        if workflow_process.status != WorkFlowProcessStatus.PENDING:
            return None
        workflow_process.note = note
        workflow_process.user = writer
        if passed:
            workflow_process.status = WorkFlowProcessStatus.APPROVED
            workflow_process.save()
            # next_approver需要通过某种统一的方式来获取
            next_workflow_process = self._gen_next_node(workflow_process)
            workflow_process = next_workflow_process if next_workflow_process is not None else workflow_process
        else:
            workflow_process.status = WorkFlowProcessStatus.REJECTED
            workflow_process.save()
            workflow_process.workflow_instance.status = WorkFlowInstanceStatus.STOP
            workflow_process.workflow_instance.save()
        return workflow_process

    def init(self, content_object, applicant, approver, name=""):
        """
        初始化审批节点
        """
        self._disable_old_workflow_instance(content_object)
        workflow_process  = self._init_workflow_instance(content_object, applicant, approver, name)
        return workflow_process

    def approve(self, workflow_process, note, passed, writer):
        """
        执行审批行为， next_approver只是一个抽象审批者
        """
        self._resync(workflow_process, note, passed)
        workflow_process = self._approve(workflow_process, note, passed, writer)
        return workflow_process

    def get_approval_info(self, approver, content_obj):
        """
        获取审批id号
        """
        approval_info = {}
        content_type = ContentType.objects.get_for_model(content_obj)
        wfp = WorkFlowProcess.objects.filter(status=WorkFlowProcessStatus.PENDING, workflow_instance__content_type=content_type,
                                                     workflow_instance__object_id=content_obj.id,
                                                     workflow_instance__status__in=[WorkFlowInstanceStatus.INIT, WorkFlowInstanceStatus.DELIVER]).filter(
                                                     user=approver).first()
        if wfp is not None:
            approval_info.update({"approval_id":wfp.id, "node_name":wfp.current_node.name})
        return approval_info