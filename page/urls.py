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
    path("credit_limit", views.OdinesCreditLimitView.as_view(), name="odines-credit-limt"),
    path("customer", views.OdinesCustomerView.as_view(), name="odines-customer"),
    path("validate_selfblock", views.OdinesSelfBlockView.as_view(), name="odines-validate-selfblock"),

    path("v2/payment", views.FinikPaymentView.as_view(), name="payment"),
    path("finik/payment-webhook", views.FinikPaymentWebhookView.as_view(), name="payment-webhook"),
    path("finik/repayment-webhook", views.FinikRepaymentWebhookView.as_view(), name="repayment-webhook"),

    path("tunduk/xml", views.TundukXMLView.as_view(), name="tunduk-xml"),
    path("tunduk/bankpin/", views.TundukBankpinView.as_view(), name="tunduk-bankpin"),
    path("tunduk/socfund/permission/lookup/", views.TundukSocfundPermissionCheckView.as_view(), name="tunduk-socfund-permission-check"),
    path("tunduk/socfund/permission/init/", views.TundukSocfundPermissionInitView.as_view(), name="tunduk-socfund-permission-init"),
    path("tunduk/socfund/permission/confirm/", views.TundukSocfundPermissionConfirmView.as_view(), name="tunduk-socfund-permission-confirm"),
    path("tunduk/socfund/work-period-info-with-sum/", views.TundukWorkPeriodViewView.as_view(), name="tunduk-workperiod"),
    path("tunduk/xml/r1/central-server/GOV/70000018/sfrkr-service/TundukApiOONPhysic", views.TundukCheckView.as_view(), name="tunduk-check"),
    path("tunduk/xml/r1/central-server/GOV/70000018/sfrkr-service/PublicOfficials", views.TundukCheckView.as_view(), name="tunduk-check"),
    path("tunduk/xml/r1/central-server/GOV/70000018/sfrkr-service/TundukApiKGPhysicAll", views.TundukCheckView.as_view(), name="tunduk-check"),
    path("tunduk/xml/r1/central-server/GOV/70000018/sfrkr-service/TundukApiKGPhysic", views.TundukCheckView.as_view(), name="tunduk-check"),
    #path("",views.IndexView.as_view(), name="index"),
]
