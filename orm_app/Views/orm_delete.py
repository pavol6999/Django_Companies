
from django.db.models.aggregates import Count
from orm_app.models import OrPodanieIssues, BulletinIssues, RawIssues

def execute(request, id):
    podanie_obj_deleted = OrPodanieIssues.objects.filter(id=id).first()
    if podanie_obj_deleted == None:
        
        return {"error":{"message":"Záznam neexistuje"}}
    

    #delete from or_podanie_issues
    podanie_obj_deleted.delete()

    raw_count = OrPodanieIssues.objects.filter(raw_issue_id=podanie_obj_deleted.raw_issue_id).count()
    if raw_count == 0:
        RawIssues.objects.filter(id=podanie_obj_deleted.raw_issue_id).delete()

        bulletin_count = OrPodanieIssues.objects.filter(bulletin_issue_id=podanie_obj_deleted.bulletin_issue_id).count()

        if bulletin_count == 0:
            raw_bulletin_count = RawIssues.objects.filter(bulletin_issue_id=podanie_obj_deleted.bulletin_issue_id).count()

            if raw_bulletin_count == 0:
                BulletinIssues.objects.filter(id=podanie_obj_deleted.bulletin_issue_id).delete()

    return None