from django.urls import path

from . import views

app_name = "page"
urlpatterns = [
    path("",views.index, name="index"),
    path("get/", views.PageGetView.as_view(), name="page-get"),
    path("post/", views.PagePostView.as_view(), name="page-post"),
    path("file", views.OdinesFileView.as_view(), name="odines-file"),
    path("new_loan", views.OdinesNewLoanView.as_view(), name="odines-new-loan"),
    path("loan_schedule", views.OdinesLoanScheduleView.as_view(), name="odines-loan-schedule"),
    path("get_loans", views.OdinesGetLoansView.as_view(), name="odines-get-loans"),
    path("repayment", views.OdinesRepaymentView.as_view(), name="odines-repayment"),
    path("getcreditproducts", views.OdinesGetCreditProductsView.as_view(), name="odines-new-loan"),
    path("paymentcalculation", views.OdinesPaymentCalculationView.as_view(), name="odines-payment-calculation"),
    path("v2/payment", views.FinikPaymentView.as_view(), name="payment"),
    path("finik/payment-webhook", views.FinikPaymentWebhookView.as_view(), name="payment-webhook"),
    path("finik/repayment-webhook", views.FinikRepaymentWebhookView.as_view(), name="repayment-webhook"),
    #path("",views.IndexView.as_view(), name="index"),
]
