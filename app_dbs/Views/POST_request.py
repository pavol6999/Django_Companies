from django.db import connection
import json
from . import utils


def execute_query(request):
    params = utils.parameter_parser_post(request)
    error_list = utils.check_required_parameters(params)
    if len(error_list["errors"]) != 0:
        return error_list

    # ---------------------------------------------------------------------------------
    # INSERT INTO BULLETIN_ISSUES

    insert_bulletin_issues = f"""
        INSERT INTO 
            ov.bulletin_issues(year,number,published_at,created_at,updated_at)

        VALUES(extract(year from now()),
       (SELECT COALESCE(MAX(number),0) FROM ov.bulletin_issues WHERE year=date_part('year', CURRENT_DATE))+1,
       now(),now(),now()) RETURNING id;
    """

    with connection.cursor() as cursor:
        cursor.execute(insert_bulletin_issues)
        bulletin_issue_id = cursor.fetchone()[0]

    # -----------------------------------------------------------------------------------------
    # INSERT INTO raw_issues

    insert_raw_issues = f"""
        INSERT INTO 
            ov.raw_issues(bulletin_issue_id,file_name,content,created_at,updated_at)
        VALUES({bulletin_issue_id},'-','-',now(),now()) RETURNING id; 
    """

    with connection.cursor() as cursor:
        cursor.execute(insert_raw_issues)
        raw_issue_id = cursor.fetchone()[0]

    # -----------------------------------------------------------------------------------------
    # INSERT INTO ov.Or_podanie_issues
    address = "%s, %s %s" % (
        params["street"], params["postal_code"], params["city"])

    insert_or_podanie_issues = f"""
        INSERT INTO 
            ov.or_podanie_issues(br_mark,bulletin_issue_id,raw_issue_id,br_court_code, br_court_name, kind_code, kind_name, cin, registration_date,
            corporate_body_name, br_section, br_insertion, text, created_at, updated_at, address_line, street, postal_code, city )
        
        VALUES('-',{bulletin_issue_id},{raw_issue_id},'-',%(br_court_name)s,'-',%(kind_name)s,%(cin)s,
        %(registration_date)s,%(corporate_body_name)s,%(br_section)s,%(br_insertion)s,%(text)s,now(),now(),'{address}',
        %(street)s,%(postal_code)s,%(city)s) RETURNING id, br_court_name, kind_name, cin, registration_date, corporate_body_name, br_section, text, street, postal_code, city
                                                                
    """
   
    with connection.cursor() as cursor:
        cursor.execute(insert_or_podanie_issues, params)
        return_value = utils.dictfetchall(cursor)[0]

    return return_value


