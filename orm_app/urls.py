from orm_app.Views import orm_companies
from django.urls import path
from . import Views


urlpatterns = [
  #path('test/',Views.test.test)
  path('ov/submissions/', Views.routes.method_switch),
  path('ov/submissions/<int:id>', Views.routes.method_switch),
  path('companies/', Views.orm_companies.execute)
 
]
