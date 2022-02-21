
import math
from . import utils
from django.db.models import F,Q  
from orm_app.models import OrPodanieIssues as Podanie
from django.core.paginator import Paginator

SELECT_COLS = ["id", "br_court_name", "kind_name", "cin", "registration_date", "corporate_body_name",
                 "br_section", "br_insertion", "text", "street", "postal_code", "city"]


def create_filters(params, qs):
    if params['query'] != "":
        qs = qs.filter((Q(corporate_body_name__icontains=params['query']) | Q(city__icontains=params['query']) | Q(cin__icontains=params['query'])))
    if params['parsed_lte'] != None:
        qs = qs.filter(registration_date__lte=params['parsed_lte'])
    if params['parsed_gte'] != None:
        qs = qs.filter(registration_date__gte=params['parsed_gte'])
   
    return qs


def fetch_one(id):

    
    qs = Podanie.objects.values(*SELECT_COLS).filter(id=id).first()
    return {"response":qs if qs != None else []}

def fetch_all(request):
    params = utils.parameter_parser_get(request)
    utils.check_get_parameters(params,"get")

    qs = Podanie.objects.values(*SELECT_COLS)

    qs = create_filters(params,qs)

    

    if params['order_type'].upper() == 'ASC':
        
        value = qs.order_by(F(params['order_by']).asc(nulls_last=True))
    else:
        value = qs.order_by(F(params['order_by']).desc(nulls_last=True))

    #paginator = Paginator(value, params['per_page']) # tu sa prvykrat zavola query
    count = value.count()
    value = value[(params['page']-1)*params['per_page']:params['page']*params['per_page']]
    
    # if params[page] exceeds total pages
    #if paginator.num_pages < params['page']:
   #     page_obj = paginator.get_page(1) 
   # else:
    #    page_obj = paginator.get_page(params['page'])

    
    

    metadata = {
        "page": params["page"],
        "per_page": params["per_page"],
        "pages": math.ceil(count/params["per_page"]),
        "total": count
    }

    
    json = {"items": list(value), "metadata": metadata}
  
    return json