from django.urls import path
from . import Views


urlpatterns = [
    path('v1/health/', Views.db_uptime.uptime, name='uptime'),
    path('', Views.routes.homepage, name='index'),
    path('v1/ov/submissions/', Views.routes.method_switch),
    path('v1/ov/submissions/<int:id>', Views.DELETE_request.DELETE_method),
    path('v1/companies/', Views.companies.company_select)
]
