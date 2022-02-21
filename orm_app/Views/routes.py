
from django.http.response import HttpResponse, JsonResponse
from . import orm_get, orm_post, orm_put, orm_delete
from django.views.decorators.csrf import csrf_exempt
from datetime import date 


@csrf_exempt
def method_switch(request, id=None):
    if request.method == 'POST':
        json = orm_post.execute(request)
        if list(json.keys())[0] == "errors":
            return JsonResponse(json, status=422)
        else:
            return JsonResponse(json, status=201)

    if request.method == 'GET':
        if id != None:
            returned_value = orm_get.fetch_one(id)
        else:
            returned_value = orm_get.fetch_all(request)
        return JsonResponse(returned_value)

    if request.method == 'PUT' and id != None:
    
        json = orm_put.execute(request, id)
        if list(json.keys())[0] == "errors":
            return JsonResponse(json, status=422)
        else:
            return JsonResponse(json, status=201)

    if request.method == 'DELETE' and id != None:
        returned = orm_delete.execute(request, id)
        if returned == None:
            return HttpResponse(status=204)
        else:
            return JsonResponse(returned,status=404)