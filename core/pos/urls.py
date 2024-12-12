from django.urls import path

from core.pos.views.activity.views import *
from core.pos.views.activity_control.views import *
from core.pos.views.client.views import *
from core.pos.views.company.views import CompanyUpdateView
from core.pos.views.contract.views import *
from core.pos.views.employee.views import *
from core.pos.views.expenses.views import *
from core.pos.views.harvest_control.views import *
from core.pos.views.invoice.views import *
from core.pos.views.lot.views import *
from core.pos.views.plant.views import *
from core.pos.views.plant_type.views import *
from core.pos.views.production.views import *
from core.pos.views.provider.views import *
from core.pos.views.purchase.views import *
from core.pos.views.resource.views import *
from core.pos.views.resource_type.views import *
from core.pos.views.tape.views import *
from core.pos.views.tape_assignment.views import *
from core.pos.views.taped_fruit_control.views import *
from core.pos.views.type_expense.views import *

urlpatterns = [
    # company
    path('company/update/', CompanyUpdateView.as_view(), name='company_update'),
    # provider
    path('provider/', ProviderListView.as_view(), name='provider_list'),
    path('provider/add/', ProviderCreateView.as_view(), name='provider_create'),
    path('provider/update/<int:pk>/', ProviderUpdateView.as_view(), name='provider_update'),
    path('provider/delete/<int:pk>/', ProviderDeleteView.as_view(), name='provider_delete'),
    # client
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/add/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    # employee
    path('employee/', EmployeeListView.as_view(), name='employee_list'),
    path('employee/add/', EmployeeCreateView.as_view(), name='employee_create'),
    path('employee/update/<int:pk>/', EmployeeUpdateView.as_view(), name='employee_update'),
    path('employee/delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee_delete'),
    # contract
    path('contract/', ContractListView.as_view(), name='contract_list'),
    path('contract/add/', ContractCreateView.as_view(), name='contract_create'),
    path('contract/update/<int:pk>/', ContractUpdateView.as_view(), name='contract_update'),
    path('contract/delete/<int:pk>/', ContractDeleteView.as_view(), name='contract_delete'),
    # activity
    path('activity/', ActivityListView.as_view(), name='activity_list'),
    path('activity/add/', ActivityCreateView.as_view(), name='activity_create'),
    path('activity/update/<int:pk>/', ActivityUpdateView.as_view(), name='activity_update'),
    path('activity/delete/<int:pk>/', ActivityDeleteView.as_view(), name='activity_delete'),
    # lot
    path('lot/', LotListView.as_view(), name='lot_list'),
    path('lot/add/', LotCreateView.as_view(), name='lot_create'),
    path('lot/update/<int:pk>/', LotUpdateView.as_view(), name='lot_update'),
    path('lot/delete/<int:pk>/', LotDeleteView.as_view(), name='lot_delete'),
    # tape
    path('tape/', TapeListView.as_view(), name='tape_list'),
    path('tape/add/', TapeCreateView.as_view(), name='tape_create'),
    path('tape/update/<int:pk>/', TapeUpdateView.as_view(), name='tape_update'),
    path('tape/delete/<int:pk>/', TapeDeleteView.as_view(), name='tape_delete'),
    # type_expense
    path('type/expense/', TypeExpenseListView.as_view(), name='type_expense_list'),
    path('type/expense/add/', TypeExpenseCreateView.as_view(), name='type_expense_create'),
    path('type/expense/update/<int:pk>/', TypeExpenseUpdateView.as_view(), name='type_expense_update'),
    path('type/expense/delete/<int:pk>/', TypeExpenseDeleteView.as_view(), name='type_expense_delete'),
    # expenses
    path('expenses/', ExpensesListView.as_view(), name='expenses_list'),
    path('expenses/add/', ExpensesCreateView.as_view(), name='expenses_create'),
    path('expenses/update/<int:pk>/', ExpensesUpdateView.as_view(), name='expenses_update'),
    path('expenses/delete/<int:pk>/', ExpensesDeleteView.as_view(), name='expenses_delete'),
    # client
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/add/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    # resource_type
    path('resource/type/', ResourceTypeListView.as_view(), name='resource_type_list'),
    path('resource/type/add/', ResourceTypeCreateView.as_view(), name='resource_type_create'),
    path('resource/type/update/<int:pk>/', ResourceTypeUpdateView.as_view(), name='resource_type_update'),
    path('resource/type/delete/<int:pk>/', ResourceTypeDeleteView.as_view(), name='resource_type_delete'),
    # resource
    path('resource/', ResourceListView.as_view(), name='resource_list'),
    path('resource/add/', ResourceCreateView.as_view(), name='resource_create'),
    path('resource/update/<int:pk>/', ResourceUpdateView.as_view(), name='resource_update'),
    path('resource/delete/<int:pk>/', ResourceDeleteView.as_view(), name='resource_delete'),
    # purchase
    path('purchase/', PurchaseListView.as_view(), name='purchase_list'),
    path('purchase/add/', PurchaseCreateView.as_view(), name='purchase_create'),
    path('purchase/delete/<int:pk>/', PurchaseDeleteView.as_view(), name='purchase_delete'),
    # plant_type
    path('plant/type/', PlantTypeListView.as_view(), name='plant_type_list'),
    path('plant/type/add/', PlantTypeCreateView.as_view(), name='plant_type_create'),
    path('plant/type/update/<int:pk>/', PlantTypeUpdateView.as_view(), name='plant_type_update'),
    path('plant/type/delete/<int:pk>/', PlantTypeDeleteView.as_view(), name='plant_type_delete'),
    # plant
    path('plant/', PlantListView.as_view(), name='plant_list'),
    path('plant/add/', PlantCreateView.as_view(), name='plant_create'),
    path('plant/update/<int:pk>/', PlantUpdateView.as_view(), name='plant_update'),
    path('plant/delete/<int:pk>/', PlantDeleteView.as_view(), name='plant_delete'),
    # producction
    path('production/', ProductionListView.as_view(), name='production_list'),
    path('production/add/', ProductionCreateView.as_view(), name='production_create'),
    path('production/delete/<int:pk>/', ProductionDeleteView.as_view(), name='production_delete'),
    # tape_assignment
    path('tape/assignment/', TapeAssignmentListView.as_view(), name='tape_assignment_list'),
    path('tape/assignment/add/', TapeAssignmentCreateView.as_view(), name='tape_assignment_create'),
    path('tape/assignment/delete/<int:pk>/', TapeAssignmentDeleteView.as_view(), name='tape_assignment_delete'),
    # activity_control
    path('activity/control/', ActivityControlListView.as_view(), name='activity_control_list'),
    path('activity/control/add/', ActivityControlCreateView.as_view(), name='activity_control_create'),
    path('activity/control/delete/<int:pk>/', ActivityControlDeleteView.as_view(), name='activity_control_delete'),
    # taped_fruit_control
    path('taped/fruit/control/', TapedFruitControlListView.as_view(), name='taped_fruit_control_list'),
    path('taped/fruit/control/add/', TapedFruitControlCreateView.as_view(), name='taped_fruit_control_create'),
    path('taped/fruit/control/delete/<int:pk>/', TapedFruitControlDeleteView.as_view(), name='taped_fruit_control_delete'),
    # harvest_control
    path('harvest/control/', HarvestControlListView.as_view(), name='harvest_control_list'),
    path('harvest/control/add/', HarvestControlCreateView.as_view(), name='harvest_control_create'),
    path('harvest/control/delete/<int:pk>/', HarvestControlDeleteView.as_view(), name='harvest_control_delete'),
    # invoice
    path('invoice/', InvoiceListView.as_view(), name='invoice_list'),
    path('invoice/add/', InvoiceCreateView.as_view(), name='invoice_create'),
    path('invoice/delete/<int:pk>/', InvoiceDeleteView.as_view(), name='invoice_delete'),
    path('invoice/print/<int:pk>/', InvoicePrintView.as_view(), name='invoice_print'),
]
