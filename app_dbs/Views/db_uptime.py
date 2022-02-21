from django.shortcuts import render
from django.db import connection
import json
from django.http import JsonResponse
# Create your views here.




def uptime(request):
    with connection.cursor() as cursor:
        uptime_query = "SELECT date_trunc('second', current_timestamp - pg_postmaster_start_time()) as uptime; "
        cursor.execute(uptime_query)
        return_value = str(cursor.fetchone()[0]).replace(",","")
    return JsonResponse({"pgsql": {"uptime": return_value}})






