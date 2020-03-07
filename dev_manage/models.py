from django.db import models

# Create your models here.

class NodeInfo(models.Model):

    # 节点编号
    node_Num = models.CharField(max_length=50)

    # 节点IP
    node_IP = models.CharField(max_length=50)

    # 节点MAC
    node_MAC = models.CharField(max_length=50)

    # 节点在线状态
    node_Status = models.CharField(max_length=50)

    # 节点权限
    node_Power = models.CharField(max_length=50)

    # 节点类型(发送/接收)
    node_Type = models.CharField(max_length=50)

    def __unicode__(self):
        return self.node_MAC
