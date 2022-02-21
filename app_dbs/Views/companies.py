import math

from django.http.response import JsonResponse
from . import utils
from django.db import connection

def full_text(query_text):
    if query_text != "":
        return "( name ~* %(query)s  OR  address_line ~* %(query)s )"
    return ""


def company_select(request):
    params = utils.parameter_parser_get(request)
    utils.check_get_parameters(params,"companies")
    

    lte, gte = utils.dates_to_where_companies(
        params["parsed_lte"], params["parsed_gte"])
    searched_text = full_text(params['query'])
    WHERE = utils.where_condition(lte, gte, searched_text)

    query = """

      
            WITH tbl1 AS 
        (
            SELECT 
                cin,count(*) as konkurz_restrukturalizacia_actors_count
            FROM 
                ov.konkurz_restrukturalizacia_actors
            WHERE 
                cin IS NOT NULL and cin != 0
            GROUP BY cin
        ),
        tbl2 as 
        (
            SELECT 
                cin, count(*) as likvidator_issues_count
            FROM 
                ov.likvidator_issues 
            WHERE 
                cin IS NOT NULL and cin != 0
            GROUP BY cin
        ),
        tbl3 as 
        (
            SELECT 
                cin, count(*) as or_podanie_issues_count
            FROM 
                ov.or_podanie_issues 
            WHERE 
                cin IS NOT NULL and cin != 0
            GROUP BY cin
        ),
        tbl4 as 
        (
            SELECT 
                cin, count(*) as znizenie_imania_issues_count
            FROM 
                ov.znizenie_imania_issues 
            WHERE 
                cin IS NOT NULL and cin != 0
            GROUP BY cin
        ),
        tbl5 as 
        (
            SELECT 
                cin, count(*) as konkurz_vyrovnanie_issues_count
            FROM 
                ov.konkurz_vyrovnanie_issues
            WHERE 
                cin IS NOT NULL and cin != 0
            GROUP BY cin
        )
        SELECT companies.cin, name, br_section, address_line, last_update, or_podanie_issues_count,znizenie_imania_issues_count,likvidator_issues_count,konkurz_vyrovnanie_issues_count,konkurz_restrukturalizacia_actors_count
        FROM ov.companies
        LEFT JOIN tbl1 ON companies.cin = tbl1.cin
        LEFT JOIN tbl2 ON companies.cin = tbl2.cin
        LEFT JOIN tbl3 ON companies.cin = tbl3.cin
        LEFT JOIN tbl4 ON companies.cin = tbl4.cin
        LEFT JOIN tbl5 ON companies.cin = tbl5.cin
        
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

    query_count = """
            SELECT count(*) FROM ov.companies
        """
    if WHERE:
        query_count += WHERE

    curor = connection.cursor()
    with connection.cursor() as cursor:
        
        cursor.execute(query, params)
        print(query % params)
        return_value = utils.dictfetchall(cursor)

        cursor.execute(query_count, params)
        print(query_count % params)
        return_count = cursor.fetchone()[0]

    metadata = {
        "page": params["page"],
        "per_page": params["per_page"],
        "pages": math.ceil(return_count/params["per_page"]),
        "total": return_count
    }
    json = {"items": return_value, "metadata": metadata}

    return JsonResponse(json)
