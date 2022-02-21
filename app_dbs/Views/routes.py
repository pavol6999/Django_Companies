from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.utils.dateparse import parse_date, parse_datetime
from django.views.decorators.csrf import csrf_exempt
from . import GET_request, POST_request


def homepage(request):
    return render(request, "pages/home.html")


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)


@csrf_exempt
def method_switch(request):
    if request.method == 'POST':
        json = POST_request.execute_query(request)
        if list(json.keys())[0] == "errors":
            return JsonResponse(json, status=422)
        else:
            return JsonResponse({"response": json}, status=201)

    if request.method == 'GET':
        json = GET_request.execute_get(request)
        return JsonResponse(json)
