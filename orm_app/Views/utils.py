import json
from django.utils.dateparse import parse_date, parse_datetime
from django.utils.datetime_safe import datetime, strftime


ORDER_GET = ["id", "br_court_name", "kind_name", "cin", "registration_date", "corporate_body_name",
                 "br_section", "br_insertion", "text", "street", "postal_code", "city"]
 

ORDER_BY_COMP = ["companies.cin", "name", "br_section", "address_line", "last_update", "created_at", "updated_at", "or_podanie_issues_count","znizenie_imania_issues_count","likvidator_issues_count","konkurz_vyrovnanie_issues_count","konkurz_restrukturalizacia_actors_count"]







def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def parameter_parser_post(request):
    if request.body == b'':
        return {}
    parameters = json.loads(request.body)
    params = {
        "cin": parameters.get("cin", ""),
        "registration_date": parameters.get("registration_date", ""),
        "br_court_name": parameters.get("br_court_name", ""),
        "kind_name": parameters.get("kind_name", ""),
        "corporate_body_name": parameters.get("corporate_body_name", ""),
        "br_section": parameters.get("br_section", ""),
        "br_insertion": parameters.get("br_insertion", ""),
        "text": parameters.get("text", ""),
        "street": parameters.get("street", ""),
        "postal_code": parameters.get("postal_code", ""),
        "city": parameters.get("city", "")
        
        }
    return params


def parameter_parser_get(request):
    params = {
        "page": request.GET.get("page", 1),
        "per_page": request.GET.get("per_page", 10),
        "order_by": request.GET.get("order_by", "id"),
        "order_type": request.GET.get("order_type", "DESC"),

        "parsed_lte": check_datetime(request.GET.get("registration_date_lte" if request.path == '/v2/ov/submissions/' else "last_update_lte", "")),
        "parsed_gte": check_datetime(request.GET.get("registration_date_gte" if request.path == '/v2/ov/submissions/' else "last_update_gte", "")),
        "query": request.GET.get("query", "")
    }
    return params

def check_put_parameters(params):
    error_list = {"errors": []}


    

    for key, value in params.items():

        if key == 'cin' and type(value) != int:
            error_list["errors"].append({"field": "cin","reasons": ["not_number"]})

        if key == 'registration_date':
            try:
                parsed_date = check_datetime(params["registration_date"])
                if (parsed_date != None and parsed_date.year != 2021) or parsed_date == None:
                    error_list["errors"].append({"field": "registration_date","reasons": ["invalid_range"]})
            except ValueError:
                error_list["errors"].append({"field": "registration_date","reasons": ["invalid_range"]})

        if key != 'cin' and key != 'registration_date' and type(value) != str:
            error_list["errors"].append({"field": key,"reasons": ["not_string"]})
    
    return error_list


def check_required_parameters(params):

    error_list = {"errors": []}

    try:
        parsed_date = check_datetime(params["registration_date"])
        if parsed_date != None and parsed_date.year != 2021:
            params["registration_date"] = ""
    except ValueError:
        params["registration_date"] = ""

    if type(params["cin"]) != int:

        error_list["errors"].append({
            "field": "cin",
            "reasons": ["required"] if params["cin"] == "" else ["required", "not_number"]
        })

    if parsed_date == "" or parsed_date == None:
        error_list["errors"].append({
            "field": "registration_date",
            "reasons": ["required"] if params["registration_date"] == "" else ["required", "invalid_range"]
        })

    for param in list(params.items())[2:]:
        if not param[1] or type(param[1]) != str:
            error_list["errors"].append({
                "field": param[0],
                "reasons": ["required"] if not param[1] else ["required", "not_string"]
            })

    return error_list


# verify parameters from GET request, set default value if the parameter is wrong
def check_get_parameters(params,method):

    try:
        params["page"] = int(params["page"])
    except ValueError:
        params["page"] = 1

    if params["page"] < 1:
        params["page"] = 1

    try:
        params["per_page"] = int(params['per_page'])
    except ValueError:
        params["per_page"] = 10

    if params["per_page"] < 1:
        params["per_page"] = 10

    if method == 'get':
        if params["order_by"].lower() not in ORDER_GET:
            params["order_by"] = "id"

    if method == "companies":
        if params["order_by"].lower() not in ORDER_BY_COMP:
            params["order_by"] = "cin"

    if params["order_type"].upper() not in ["ASC", "DESC"]:
        params["order_type"] = "DESC"

    else:
        params["order_orm"] = params['order_by']

    if params["parsed_lte"] != None:

        params["parsed_lte"] = params["parsed_lte"].date() if type(params["parsed_lte"]) == datetime.date else  params["parsed_lte"]

    if params["parsed_gte"] != None:
        params["parsed_gte"] = params["parsed_gte"].date() if type(params["parsed_gte"]) == datetime.date else  params["parsed_gte"]
    params['offset'] = (params['page']-1)*params['per_page']

# verify correct datetime


def check_datetime(datetime):

    if type(datetime) != str:
        return None
    #2012-02-02 14:22:36
    if ' ' in datetime or 'T' in datetime:
        try:
            parsed_datetime = parse_datetime(datetime)
            
        except ValueError:
            parsed_datetime = None

    #2012-02-02
    else:
        try: 
            parsed_datetime = parse_date(datetime)
        except ValueError:
            parsed_datetime = None
        
    return parsed_datetime
