
from django.db import connection
from . import utils
from django.utils.datetime_safe import strftime
import math

ORDER_BY_COLS = ["id", "br_court_name", "kind_name", "cin", "registration_date", "corporate_body_name",
                 "br_section", "br_insertion", "text", "street", "postal_code", "city"]
SELECT_COLS = ",".join(ORDER_BY_COLS)


def full_text(query_search):
    if query_search != "":
        return " ( corporate_body_name ~* %(query)s  OR cin::text ~* %(query)s OR city ~* %(query)s ) "
    return ""


def execute_get(request):

    params = utils.parameter_parser_get(request)

    utils.check_get_parameters(params,"get")

    lte, gte = utils.dates_to_where(params["parsed_lte"], params["parsed_gte"])
    searched_text = full_text(params["query"])
    WHERE = utils.where_condition(lte, gte, searched_text)

    query = f"""
            SELECT 
                {SELECT_COLS}
            FROM 
                ov.or_podanie_issues
            """

    if WHERE:
        query += WHERE

    query += """ ORDER BY """ + params["order_by"] + " " + params["order_type"]

    query += """ 
            NULLS LAST
            LIMIT 
                %(per_page)s
            OFFSET
                %(offset)s ;
            """
    query_count = f"""
            SELECT 
                COUNT(*)
            FROM 
                ov.or_podanie_issues
            """
    if WHERE:
        query_count += WHERE

  
    with connection.cursor() as cursor:

        cursor.execute(query, params)
        return_value = utils.dictfetchall(cursor)

        cursor.execute(query_count,params)
        count = utils.dictfetchall(cursor)

    
    metadata = {
        "page": params["page"],
        "per_page": params["per_page"],
        "pages": math.ceil(count[0]['count']/params["per_page"]),
        "total": count[0]['count']
    }
    json = {"info": return_value, "metadata": metadata}
    return json
