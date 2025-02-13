from django.contrib import admin
from django.urls import path
from quotation_requests.views import add_equipment, cancel_quotation_request
from quotation_requests import views

from quotation_requests.views import (
    QuotationRequestsListView,
    QuotationRequestsCreateView,
    QuotationRequestsUpdateView,
    QuotationRequestsDeleteView,
)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", QuotationRequestsListView.as_view(), name="quotationrequests_list"),
    path("create", QuotationRequestsCreateView.as_view(), name="quotationrequests_create"),
    path("update/<int:pk>", QuotationRequestsUpdateView.as_view(), name="quotationrequests_update"),
    path("delete/<int:pk>", QuotationRequestsDeleteView.as_view(), name="quotationrequests_delete"), 
    path('add_equipment/<int:pk>', add_equipment, name='add_equipment'),
    path('cancel/<int:pk>', cancel_quotation_request, name='cancel_quotation_request'),
]