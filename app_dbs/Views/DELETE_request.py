from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection


@csrf_exempt
def DELETE_method(request,id):

   
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM ov.or_podanie_issues WHERE id=%s;",(id,))
        number = cursor.fetchone()[0]
    if number == 0:
        return JsonResponse({"error":{"message":"Záznam neexistuje"}}, status=404)


    with connection.cursor() as cursor:

        #delete from or_podanie_issues
        cursor.execute("DELETE FROM ov.or_podanie_issues WHERE id = %s RETURNING bulletin_issue_id, raw_issue_id;",(id,))
        bulletin_issue_id, raw_issue_id = cursor.fetchone()[:2]
        
    

        #find all raw id inside or_podanie_issues
        cursor.execute("SELECT COUNT(*) FROM ov.or_podanie_issues WHERE raw_issue_id=%s;",(raw_issue_id,))
        count_raw_id = cursor.fetchone()[0]

        if count_raw_id == 0:
            cursor.execute("DELETE FROM ov.raw_issues WHERE id=%s",(raw_issue_id,))


            #find all bulletin issues id inside or_podanie_issues
            cursor.execute("SELECT COUNT(*) FROM ov.or_podanie_issues WHERE bulletin_issue_id=%s;",(bulletin_issue_id,))
            count_bulletin_id = cursor.fetchone()[0]


            if count_bulletin_id == 0:
                cursor.execute("SELECT COUNT(*) FROM ov.raw_issues WHERE bulletin_issue_id = %s",(bulletin_issue_id,))
                count_bulletin_id_raw = cursor.fetchone()[0]
                if count_bulletin_id_raw == 0:
                    cursor.execute("DELETE FROM ov.bulletin_issues WHERE id=%s",(bulletin_issue_id,))
      
    return HttpResponse(status=204)


