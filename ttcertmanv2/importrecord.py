import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

import django
from datetime import datetime
import ttcertmanv2.models



def controltype(paramdb):
    t = ttcertmanv2.models.CertControl.objects.get_or_create(cert_control=paramdb)[0]
    return t


def certtype(paramdb):
    t = ttcertmanv2.models.CertType.objects.get_or_create(cert_type=paramdb)[0]
    return t


def certstatus(days):
    if 90 >= days >= 20:
        t = "alert"
    elif 20 > days >= 1:
        t = "warning"
    elif days == 0:
        t = "expired"
    else:
        t = "clear"
    cstatus = ttcertmanv2.models.CertStatus.objects.get_or_create(cert_status=t)[0]
    return cstatus


def certid(paramdb):
    t = ttcertmanv2.models.CertId.objects.get_or_create(cert_id=paramdb)[0]
    return t


def update_cert(detail_cert, host, port, control_type, cert_type):
    cert_date = datetime.now()
    control_type = controltype(control_type)
    cert_type = certtype(cert_type)
    cert_id = certid(host)
    cert_hostname = detail_cert[0]
    cert_scan_port = port
    cert_issuer = detail_cert[1]
    cert_cn = detail_cert[0]
    cert_days = detail_cert[3]
    cert_status = certstatus(detail_cert[3])
    ScanRecord = ttcertmanv2.models.CertScanRecord.objects.update_or_create(
        cert_id=cert_id,
        defaults={'control_type': control_type, 'cert_type': cert_type, 'cert_hostname': cert_hostname,
                  'cert_scan_port': cert_scan_port,
                  'cert_issuer': cert_issuer, 'cert_cn': cert_cn, 'cert_status': cert_status, 'cert_days': cert_days,
                  'cert_date': cert_date})