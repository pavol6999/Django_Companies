import datetime
from django.db.models import Max
from django.db.models.expressions import Subquery
from . import utils
from orm_app.models import OrPodanieIssues, BulletinIssues, RawIssues
from django.db.models.functions import Now
from django.utils import timezone

def create_json(podanie_obj):
    json = {
        "response": {
            "id": podanie_obj.id,
            "br_court_name": podanie_obj.br_court_name,
            "kind_name": podanie_obj.kind_name,
            "cin": podanie_obj.cin,
            "registration_date": podanie_obj.registration_date,
            "corporate_body_name": podanie_obj.corporate_body_name,
            "br_section": podanie_obj.br_section,
            "text":podanie_obj.text,
            "street": podanie_obj.street,
            "postal_code": podanie_obj.postal_code,
            "city": podanie_obj.city
        }
    }
    return json

def execute(request):
    params = utils.parameter_parser_post(request)
    error_list = utils.check_required_parameters(params)
    if len(error_list["errors"]) != 0:
        return error_list


    now = timezone.now()

    # insert into bulletin_issues
    number = BulletinIssues.objects.filter(year=now.year).aggregate(Max('number'))
    bulletin_obj = BulletinIssues.objects.create(year=now.year,
                                                 published_at=now,
                                                 created_at=now,
                                                 updated_at=now, 
                                                 number=number['number__max']+1)

    # insert into raw_issues
    raw_obj = RawIssues.objects.create(bulletin_issue=bulletin_obj,
                                       file_name='-', 
                                       content='-', 
                                       created_at=now, 
                                       updated_at=now)
   

    params['br_mark'] = '-'
    params['br_court_code'] = '-'
    params['kind_code'] = '-'
    params['created_at'] = now 
    params['updated_at'] = now
    params['bulletin_issue'] = bulletin_obj
    params['raw_issue'] = raw_obj  
    params['address_line'] = "%s, %s %s" % (
        params["street"], params["postal_code"], params["city"])
    podanie_obj = OrPodanieIssues.objects.create(**params) 
    return create_json(podanie_obj)
    
    