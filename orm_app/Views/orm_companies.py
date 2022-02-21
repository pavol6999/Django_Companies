
import math
from django.core.paginator import Paginator
from django.db.models.aggregates import Count
from django.db.models.expressions import Subquery
from django.http.response import JsonResponse
from . import utils 
from orm_app.models import Companies
from django.db.models import F,Q  

def create_filters(params, qs):
    if params['query'] != "":
        qs = qs.filter((Q(name__icontains=params['query']) | Q(address_line__icontains=params['query']) ))
    if params['parsed_lte'] != None:
        qs = qs.filter(last_update__lte=params['parsed_lte'])
    if params['parsed_gte'] != None:
        qs = qs.filter(last_update__gte=params['parsed_gte'])
    
    
    return qs

def execute(request):
    params = utils.parameter_parser_get(request)
    utils.check_get_parameters(params,"companies")

    companies = Companies.objects.values("cin", "name", "br_section", "address_line", "last_update")
    companies = create_filters(params,companies)
    count = companies.count()

    companies = companies.annotate(or_podanie_issues_count=Count('orpodanieissues',distinct=True))#.order_by('or_podanie_issues_count')
    companies = companies.annotate(znizenie_imania_issues_count=Count('znizenieimaniaissues',distinct=True))#.order_by('znizenie_imania_issues_count')
    companies = companies.annotate(likvidator_issues_count=Count('likvidatorissues',distinct=True))#.order_by('likvidator_issues_count')
    companies = companies.annotate(konkurz_vyrovnanie_issues_count=Count('konkurzvyrovnanieissues',distinct=True))#.order_by('konkurz_vyrovnanie_issues_count')
    companies = companies.annotate(konkurz_restrukturalizacia_actors_count=Count('konkurzrestrukturalizaciaactors',distinct=True))#.order_by('konkurz_restrukturalizacia_actors_count')
    
    
    
    

    

    

    ## zoradenie zaznamov
    if params['order_type'].upper() == 'ASC':  
        companies = companies.order_by(F(params['order_by']).asc(nulls_last=True))
    else:
        companies = companies.order_by(F(params['order_by']).desc(nulls_last=True))

    value = companies[(params['page']-1)*params['per_page']:params['page']*params['per_page']]

    
    
    metadata = {
        "page": params["page"],
        "per_page": params["per_page"],
        "pages": math.ceil(count/params["per_page"]),
        "total": count
    }


    json = {"items": list(value), "metadata": metadata}
    return JsonResponse(json)
