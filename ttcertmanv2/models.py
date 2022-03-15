from django.db import models

class platformInfo(models.Model):
    platform_id = models.IntegerField(primary_key=True) #primary key
    platform_name = models.CharField(max_length=255)
    platform_owner = models.CharField(max_length=255)
    platform_email = models.CharField(max_length=255)

class serviceInfo(models.Model):
    service_id = models.IntegerField(primary_key=True)
    service_name = models.CharField(max_length=255)
    platform_id = models.ForeignKey(platformInfo,on_delete=models.PROTECT)

class urlControl(models.Model):
    url_control_id = models.IntegerField(primary_key=True) #primary key
    service_id = models.ForeignKey(serviceInfo,on_delete=models.PROTECT)
    url = models.CharField(max_length=255)
    port = models.IntegerField()

class networkScan(models.Model):
    network_scan_id = models.IntegerField(primary_key=True) #primary key
    ip_range = models.IntegerField()
    port_range = models.IntegerField()

class scanFile(models.Model):
    id = models.IntegerField(primary_key=True)
    service_id = models.ForeignKey(serviceInfo,on_delete=models.PROTECT) # *---------------
    cert_file_base64 = models.CharField(max_length=2048)

class controlType(models.Model):
    control_type_id = models.IntegerField() #primary key
    File = models.CharField(max_length=255)
    PortScan = models.IntegerField()
    URL = models.CharField(max_length=255)

class status(models.Model):
    chart_status_id = models.IntegerField(primary_key=True) #primary key
    expired = models.IntegerField()
    Alert = models.IntegerField()
    Warning = models.IntegerField()
    Clear = models.IntegerField()

class genesisCertificate(models.Model):
    cert_id = models.IntegerField(primary_key=True)
    cert_serial = models.CharField(max_length=128,unique=True) #unique key
    cert_name = models.CharField(max_length=255,unique=True) #unique key
    cert_signature = models.CharField(max_length=2048)
    cert_issuer = models.CharField(max_length=255)
    cert_valid_from = models.DateTimeField() #date time
    cert_valid_to = models.DateTimeField()
    cert_subject = models.CharField(max_length=255)
    cert_san = models.TextField() #text

class scanRecords(models.Model):
    cert_child_id = models.IntegerField(primary_key=True) #primary key
    cert_serial = models.ForeignKey(genesisCertificate, to_field='cert_serial',on_delete=models.PROTECT, max_length=128)
    cert_control_type_id = models.ForeignKey(controlType,on_delete=models.PROTECT)
    cert_hostname = models.CharField(max_length=255) # ------------- Unique OLMAMALI
    cert_port = models.IntegerField()
    cert_status_id = models.ForeignKey(status,on_delete=models.PROTECT)
    cert_expire_days = models.IntegerField()
    cert_service_id = models.ForeignKey(serviceInfo,on_delete=models.PROTECT)


