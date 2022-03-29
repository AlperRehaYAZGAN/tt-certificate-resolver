# Django admin.py
from django.contrib import admin
from ttcertmanv2.models import controlType, status, scanFile, genesisCertificate, networkScan, serviceInfo, platformInfo, scanRecords, urlControl


admin.site.register(controlType)
admin.site.register(status)
admin.site.register(scanFile)
admin.site.register(genesisCertificate)
admin.site.register(networkScan)
admin.site.register(serviceInfo)
admin.site.register(platformInfo)
admin.site.register(scanRecords)
admin.site.register(urlControl)
