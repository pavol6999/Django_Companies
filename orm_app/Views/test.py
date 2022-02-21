


from django.http.response import JsonResponse

from orm_app.models import BulletinIssues



def test(request):
    test = list(BulletinIssues.objects.all().values())[:10]
    return JsonResponse(test, safe=False)