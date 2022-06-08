from django.urls import path

from . import views

urlpatterns = [
    path("corps/", views.CompanyListView.as_view(), name="company_list"),
    path("esgscore/<str:ric_code>/", views.CompanyRetriveView.as_view(), name="company_detail"),

]
