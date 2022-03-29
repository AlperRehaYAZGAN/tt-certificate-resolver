from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, MaxLengthValidator, ip_address_validators, EmailValidator, URLValidator, validate_ipv4_address
import uuid

class platformInfo(models.Model):
    platform_id = models.IntegerField(primary_key=True, editable=False, verbose_name="Platform ID")
    platform_name = models.CharField(max_length=255, editable=True, verbose_name="Platform Name")
    platform_owner = models.CharField(max_length=255, editable=True, verbose_name="Platform Owner")
    platform_email = models.CharField(max_length=255, editable=True, verbose_name="Platform Email")

    class Meta:
        ordering = ['platform_id']
        verbose_name = "Platform Info"

    def __str__(self):
        return str(self.platform_id) + ": " + self.platform_name + " (" + self.platform_owner + ")"

class serviceInfo(models.Model):
    service_id = models.IntegerField(primary_key=True, editable=False, verbose_name="Service ID")
    service_name = models.CharField(max_length=255, editable=True, verbose_name="Service Name")
    platform_id = models.ForeignKey(platformInfo,on_delete=models.PROTECT, verbose_name="Platform ID")

    class Meta:
        ordering = ['service_id']
        verbose_name = "Service Info"
    
    def __str__(self):
        return str(self.service_id) + ": " + self.service_name + " (" + str(self.platform_id) + ")"

class urlControl(models.Model):
    url_control_id = models.IntegerField(primary_key=True, editable=False, verbose_name="URL Control ID")
    service_id = models.ForeignKey(serviceInfo,on_delete=models.PROTECT, verbose_name="Service ID")
    url = models.CharField(max_length=255, verbose_name="URL")
    port = models.IntegerField(verbose_name="Port", default=443, editable=False)

    class Meta:
        ordering = ['url_control_id']
        verbose_name = "URL Control"
    
    def __str__(self):
        return str(self.url_control_id) + ": " + self.url + " (" + str(self.service_id) + ")"



class networkScan(models.Model):
    network_scan_id = models.IntegerField(primary_key=True, editable=False, verbose_name="Network Scan ID")
    ip_range = models.IntegerField(unique=False, editable=True, verbose_name="IP Range")
    port_range = models.IntegerField(unique=False, editable=True, verbose_name="Port Range")

    class Meta:
        ordering = ['network_scan_id']
        verbose_name = "Network Scan"
    
    def __str__(self):
        return str(self.network_scan_id) + ": " + str(self.ip_range) + "." + str(self.port_range)

class scanFile(models.Model):
    id = models.IntegerField(primary_key=True, editable=False, verbose_name="Scan File ID")
    service_id = models.ForeignKey(serviceInfo,on_delete=models.PROTECT, verbose_name="Service ID")
    cert_file_base64 = models.CharField(max_length=2048, unique=False, editable=True, verbose_name="Cert File Base64", null=False)

    class Meta:
        ordering = ['id']
        verbose_name = "Scan File"
    
    def __str__(self):
        return str(self.id) + ": " + str(self.service_id)

class controlType(models.Model):
    control_type_id = models.IntegerField(primary_key=True, editable=False, verbose_name="Control Type ID")
    File = models.CharField(max_length=255, unique=False, editable=True, verbose_name="File")
    PortScan = models.IntegerField(unique=False, editable=True, verbose_name="Port Scan")
    URL = models.CharField(max_length=255, unique=False, editable=True, verbose_name="URL", null=False, validators=[URLValidator()])

    class Meta:
        ordering = ['control_type_id']
        verbose_name = "Control Type"
    
    def __str__(self):
        return str(self.control_type_id) + ": " + self.File + " (" + str(self.PortScan) + ")"

class status(models.Model):
    chart_status_id = models.UUIDField(primary_key=True, default=uuid.uuid4(),editable=False, verbose_name="Status ID")
    expired = models.CharField(max_length=255,editable=True,verbose_name="Status: Expired")
    alert = models.CharField(max_length=255,editable=True,verbose_name="Status: Alert")
    warning = models.CharField(max_length=255,editable=True,verbose_name="Status: Warning")
    clear = models.CharField(max_length=255,editable=True,verbose_name="Status: Clear")
    class Meta:
        ordering = ['chart_status_id']
        verbose_name = "Chart Status"
    
    def __str__(self):
        return str(self.chart_status_id) + ": " + str(self.expired) + " (" + str(self.Alert) + ")"


class genesisCertificate(models.Model):
    cert_id = models.IntegerField(primary_key=True, default=uuid.uuid4(),editable=False,verbose_name="Certificate ID")
    cert_serial = models.CharField(max_length=128,unique=True,verbose_name="Serial Number", null=False, validators=[MinLengthValidator(1), MaxLengthValidator(5)])
    cert_name = models.CharField(max_length=255,unique=True,editable=True,verbose_name="Certificate Name")
    cert_signature = models.CharField(max_length=2048, unique=True,verbose_name="Certificate Signature")
    cert_issuer = models.CharField(max_length=255,editable=True,verbose_name="Certificate Issuer")
    cert_valid_from = models.DateTimeField(editable=True,verbose_name="Valid From")
    cert_valid_to = models.DateTimeField(editable=True,verbose_name="Valid To")
    cert_subject = models.CharField(max_length=255,editable=True,verbose_name="Certificate Subject")
    cert_san = models.TextField(editable=True,verbose_name="SAN")

    class Meta:
        ordering = ['cert_valid_to']
        verbose_name = "Certificate"

    def __str__(self):
        return str(self.cert_id) + ": " + self.cert_name + " (" + self.cert_serial + ")"


class scanRecords(models.Model):
    cert_child_id = models.IntegerField(primary_key=True, editable=False, verbose_name="Certificate Child ID")
    cert_serial = models.ForeignKey(genesisCertificate, to_field='cert_serial',on_delete=models.PROTECT, max_length=128, verbose_name="Certificate Serial")
    cert_control_type_id = models.ForeignKey(controlType,on_delete=models.PROTECT, verbose_name="Control Type ID")
    cert_hostname = models.CharField(max_length=255, unique=False, editable=True, verbose_name="Hostname")
    cert_port = models.IntegerField(unique=False, editable=True, verbose_name="Port")
    cert_status_id = models.ForeignKey(status,on_delete=models.PROTECT, verbose_name="Status ID")
    cert_expire_days = models.IntegerField(unique=False, editable=True, verbose_name="Expire Days")
    cert_service_id = models.ForeignKey(serviceInfo,on_delete=models.PROTECT, verbose_name="Service ID")


