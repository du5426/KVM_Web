from django.db import models

# Create your models here.

class NodeInfo(models.Model):
    node_Num = models.CharField(max_length=50)
    node_IP = models.CharField(max_length=50)
    node_MAC = models.CharField(max_length=50)
    node_Status = models.CharField(max_length=50)
    node_Power = models.CharField(max_length=50)
    node_Type = models.CharField(max_length=50)

    def __unicode__(self):
        return self.node_MAC
