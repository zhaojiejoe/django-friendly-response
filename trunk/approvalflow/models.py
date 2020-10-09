from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import datetime
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.


class WorkFlow(models.Model):
    name = models.CharField('审批流名称', max_length=50, unique=True)
    date_created = models.DateTimeField('创建日期', auto_now_add=True)
    date_updated = models.DateTimeField('更新日期', auto_now=True)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ['-id']
        verbose_name = 'WorkFlow'
        verbose_name_plural = verbose_name


class WorkFlowNodeType:
    START = 1
    BRANCH = 2
    END = 3


class WorkFlowNode(models.Model):
    NTYPE_CHOICE = ((WorkFlowNodeType.START, '开始节点'),
                    (WorkFlowNodeType.BRANCH, '分支节点'),
                    (WorkFlowNodeType.END, '结束节点'),)
    workflow = models.ForeignKey(WorkFlow, on_delete=models.PROTECT)
    name = models.CharField('审批流节点名称', max_length=50)
    node_type = models.SmallIntegerField(choices=NTYPE_CHOICE)
    prev_node = models.ForeignKey(
        'WorkFlowNode', related_name="prev_node_wnode", null=True, on_delete=models.PROTECT)
    next_node = models.ForeignKey(
        'WorkFlowNode', related_name="next_node_wnode", null=True, on_delete=models.PROTECT)
    # 视具体情况可配置默认审批user/group/role等
    date_created = models.DateTimeField('创建日期', auto_now_add=True)
    date_updated = models.DateTimeField('更新日期', auto_now=True)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ['-id']
        verbose_name = 'WorkFlowNode'
        verbose_name_plural = verbose_name


class WorkFlowInstanceStatus:
    INIT = 1
    DELIVER = 2
    FINISH = 3
    STOP = 4


class WorkFlowInstance(models.Model):
    STATUS_CHOICE = ((WorkFlowInstanceStatus.INIT, '未发起'),
                     (WorkFlowInstanceStatus.DELIVER, '正在流转'),
                     (WorkFlowInstanceStatus.FINISH, '已完成'),
                     (WorkFlowInstanceStatus.STOP, '流转终止'),)
    name = models.CharField('审批名称', max_length=50)
    user = models.ForeignKey(User, verbose_name="发起审批者", on_delete=models.PROTECT)
    content_type = models.ForeignKey(ContentType,
                                     verbose_name="关联的数据表名", on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField("关联的表中的数据行ID")
    content_object = GenericForeignKey('content_type', 'object_id')
    is_new = models.BooleanField('是否是最新记录', default=True)
    workflow = models.ForeignKey(WorkFlow, on_delete=models.PROTECT)
    status = models.SmallIntegerField(choices=STATUS_CHOICE)
    date_created = models.DateTimeField('创建日期', auto_now_add=True)
    date_updated = models.DateTimeField('更新日期', auto_now=True)

    def __str__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        if self.name is None:
            self.name = "{0}-{1}-{2}".format(self.workflow.name,
                                             self.user.username, datetime.datetime.now())
        if not self.id:      
            WorkFlowInstance.objects.filter(content_type=self.content_type, object_id=self.object_id).update(is_new=False)
        super(WorkFlowInstance, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-id']
        verbose_name = 'WorkFlowInstance'
        verbose_name_plural = verbose_name


class WorkFlowProcessStatus:
    PENDING = 1
    APPROVED = 2
    REJECTED = 3


class WorkFlowProcess(models.Model):
    STATUS_CHOICE = ((WorkFlowProcessStatus.PENDING, '待审核'),
                     (WorkFlowProcessStatus.APPROVED, '已审核'),
                     (WorkFlowProcessStatus.REJECTED, '审核不通过'),)
    workflow_instance = models.ForeignKey(WorkFlowInstance, on_delete=models.PROTECT)
    current_node = models.ForeignKey(WorkFlowNode, null=True, on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name="操作者", null=True, on_delete=models.PROTECT)
    # 视具体情况可配置审批group/role等
    status = models.SmallIntegerField(choices=STATUS_CHOICE, default=1)
    note = models.TextField('备注', null=True)
    date_created = models.DateTimeField('创建日期', auto_now_add=True)
    date_updated = models.DateTimeField('更新日期', auto_now=True)

    def __str__(self):
        return '%s' % self.current_node.name + self.get_status_display()

    class Meta:
        ordering = ['-id']
        verbose_name = 'WorkFlowProcess'
        verbose_name_plural = verbose_name
