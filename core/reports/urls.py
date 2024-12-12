from django.urls import path

from core.reports.views.harvest_control_report.views import HarvestControlReportView, HarvestControlDetailReportView
from core.reports.views.invoice_report.views import InvoiceReportView
from core.reports.views.production_report.views import ProductionReportView
from core.reports.views.purchase_report.views import PurchaseReportView
from core.reports.views.tape_assignment_report.views import TapeAssignmentReportView
from core.reports.views.taped_fruit_control_report.views import TapedFruitControlReportView
from core.reports.views.activity_control_report.views import ActivityControlReportView

urlpatterns = [
    path('purchase/', PurchaseReportView.as_view(), name='purchase_report'),
    path('invoice/', InvoiceReportView.as_view(), name='invoice_report'),
    path('production/', ProductionReportView.as_view(), name='production_report'),
    path('harvest/control/', HarvestControlReportView.as_view(), name='harvest_control_report'),
    path('harvest/control/detail/', HarvestControlDetailReportView.as_view(), name='harvest_control_detail_report'),
    path('tape/assignment/', TapeAssignmentReportView.as_view(), name='tape_assignment_report'),
    path('taped/fruit/control/', TapedFruitControlReportView.as_view(), name='taped_fruit_control_report'),
    path('activity/control/', ActivityControlReportView.as_view(), name='activity_control_report'),
]
