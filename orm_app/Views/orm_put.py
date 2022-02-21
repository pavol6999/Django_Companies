
import json
from orm_app.models import OrPodanieIssues
from . import utils
from django.forms.models import model_to_dict


def execute(request, id):
    params =  utils.parameter_parser_post(request)

    #first we get rid of empty key values in params
    params = {k: v for k, v in params.items() if v != ''}

    error_list = utils.check_put_parameters(params)
    if len(error_list["errors"]) != 0:
        return error_list
    

    if len(params) == 0:
        return {"response":OrPodanieIssues.objects.filter(id=id).values('id','br_court_name','kind_name','cin','registration_date','corporate_body_name','br_section','text','street','postal_code','city').first()}


    podanie_obj = OrPodanieIssues.objects.filter(id=id).update(**params)

    return {"response":OrPodanieIssues.objects.filter(id=id).values('id','br_court_name','kind_name','cin','registration_date','corporate_body_name','br_section','text','street','postal_code','city').first()}
