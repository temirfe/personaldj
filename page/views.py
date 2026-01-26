from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import requests
import random
import uuid


def index(request):
    """ template = loader.get_template("page/home.html")
    context = {
        "foo": 'bar',
    }
    return HttpResponse(template.render(context, request)) """
    context = {"foo": "bar"}
    return render(request, "page/home.html", context)


class PageGetView(APIView):
    def get(self, request):
        return Response({"status": "ok", "message": "GET endpoint"})


class PagePostView(APIView):
    def post(self, request):
        return Response({"status": "ok", "data": request.data})

class OdinesFileView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        return Response({"Success": True})
    
class OdinesNewLoanView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        #return Response({"Success": False},status=500)
        guid= str(uuid.uuid4())
        num_int = random.randint(100, 10000)
        loan_id= f'GO{num_int}'
        return Response({"Success": True, "Result":{"LoanGuid":guid, "LoanID":loan_id, "LoanStatus":"Выдан"}})
        """ return Response({
            'Success': False, 
            'ErrorList': ['credit line not fould'], 
            'ErrorDescription': 'Verification error', 
            'Result': {'LoanGuid': None, 'LoanID': None, 'LoanStatus': None, 'RepeatedRequest': None}}) """
        
class OdinesLoanScheduleView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        return Response({
            "Success": True,
            "ErrorList": None,
            "ErrorDescription": "",
            "repaymentSchedule": [
                {
                    "date": "2026-01-30",
                    "amount": 31.14,
                    "interestAmount": 0.38,
                    "principalAmount": 30.76,
                    "overdueAmount": 0
                },
                {
                    "date": "2026-02-20",
                    "amount": 31.14,
                    "interestAmount": 2.2,
                    "principalAmount": 28.94,
                    "overdueAmount": 0
                },
                {
                    "date": "2026-03-20",
                    "amount": 31.14,
                    "interestAmount": 1.34,
                    "principalAmount": 29.8,
                    "overdueAmount": 0
                },
                {
                    "date": "2026-04-16",
                    "amount": 31.15,
                    "interestAmount": 0.65,
                    "principalAmount": 30.5,
                    "overdueAmount": 0
                }
            ],
            "isOverdue": None,
            "nextRepaymentAmount": 0,
            "overdueAmount": 0,
            "penaltyAmount": 0,
            "prepaidAmount": 0
        })

class OdinesGetLoansView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        return Response({
            "Success": True,
            "ErrorList": None,
            "ErrorDescription": "no error",
            "loans": [
                {
                    "loanGUID": "fa920925-3642-40b6-a272-c5ef6bbaa1a1",
                    "status": "active",
                    "currency": "KGS",
                    "loanAgreementNumber": "B81026011603",
                    "term": 3,
                    "interestRate": 29,
                    "requestDate": "2026-01-16T04:40:17Z",
                    "disbursementDate": "2026-01-16",
                    "productGuid": "04582d8c-a4e0-11f0-bc5a-00155d056d8c",
                    "productName": "Онлайн кредит",
                    "amount": 120,
                    "principalBalance": 89.24,
                    "interestBalance": 0.07,
                    "principalRepaidAmount": 30.76,
                    "totalPrincipalAndInterestAmount": 124.57,
                    "prepaymentBalance": 94.62,
                    "pastDueDays": 0,
                    "actualClosingDate": ""
                },
                ]})

class OdinesRepaymentView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        return Response({"Success": True, "ErrorList": None, "ErrorDescription": "","Result":{"RepeatedRequest":False}})
    


class OdinesGetCreditProductsView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        resp = [
            {
                "guid": "04582d8c-a4e0-11f0-bc5a-00155d056d8c",
                "name": "Онлайн кредит",
                "currency": "KGS",
                "amountMin": 0,
                "amountMax": 2000000,
                "termDefault": 0,
                "termMin": 0,
                "termMax": 48,
                "interestRateDefault": 32,
                "interestRateMin": 32,
                "interestRateMax": 37,
                "penaltyDefault": 0,
                "feeRate": 0
            }
        ]

        return Response(resp)
    
class OdinesPaymentCalculationView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        from datetime import date
        import calendar

        amount = float(request.data.get("amount", 0) or 0)
        term = int(request.data.get("term", 0) or 0)
        annual_rate = 0.29
        monthly_rate = annual_rate / 12

        def add_months(d, months):
            month = d.month - 1 + months
            year = d.year + month // 12
            month = month % 12 + 1
            day = min(d.day, calendar.monthrange(year, month)[1])
            return date(year, month, day)

        if amount <= 0 or term <= 0:
            return Response(
                {
                    "Success": False,
                    "ErrorList": ["amount", "term"],
                    "ErrorDescription": "amount and term must be positive",
                }
            )

        payment_amount = amount * monthly_rate / (1 - (1 + monthly_rate) ** (-term))
        payment_amount = round(payment_amount, 2)
        effective_rate = round(((1 + monthly_rate) ** 12 - 1) * 100, 4)

        balance = amount
        schedule = []
        total_principal_interest = 0.0
        today = date.today()

        for i in range(1, term + 1):
            interest = round(balance * monthly_rate, 2)
            principal = round(payment_amount - interest, 2)
            if i == term:
                principal = round(balance, 2)
                total = round(principal + interest, 2)
            else:
                total = payment_amount
            balance = round(balance - principal, 2)
            total_principal_interest += total

            schedule_date = add_months(today, i).isoformat() + "T00:00:00"
            schedule.append(
                {
                    "date": schedule_date,
                    "principalAmount": principal,
                    "interestAmount": interest,
                    "totalAmount": total,
                }
            )

        res = {
            "Success": True,
            "ErrorList": None,
            "ErrorDescription": "no error",
            "totalPrincipalAndInterestAmount": round(total_principal_interest, 2),
            "paymentAmount": payment_amount,
            "interestRate": 29,
            "effectiveRate": effective_rate,
            "schedule": schedule,
        }
        return Response(res)
class FinikPaymentView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        return Response({"Success": True, "status": "PENDING", 'id':'111'})
    
class FinikPaymentWebhookView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        trans_id = request.data.get("transaction_id")
        status = request.data.get("status",default="SUCCEEDED")
        #return Response({"t": trans_id, "s": status})
        body1 = {
            "accountId":"3a4e85cd-9a04-4fc4-8b77-3eea407f40f9",
            "fields":{"total":18,"account.value.persacc":"+996 +996553000665"},
            "service":{"id":"07dbb2ef-ff5c-413f-a2ec-5c439ec5714d","limit":{"id":"default_limit"},
                "logo":{"url":"https://images.averspay.kg/images/services/9228f55c-c33a-42ee-8cc0-d971463f0de2.png"},
                "maxAmount":95000,"minAmount":15,"name_en":"Optima Bank by phone number","name_ky":"Оптима Банк телефон номери боюнча","name_ru":"Оптима Банк по номеру телефона",
                "requiredFields":[{"label_ky":"Телефон номерин киргизиңиз","orderNumber":0,"keyboardType":"PHONE","label_ru":"Введите номер телефона","prefix":"+996 ","minLength":9,
                                   "inputMask":"000 000 000","label_en":"Enter the phone number","maxLength":15,"fieldId":"account.value.persacc","isHidden":False},
                                   {"orderNumber":1,"keyboardType":"TEXT","value":"5428","fieldId":"service","isHidden":False},{"label_ky":"Сумма","orderNumber":2,"keyboardType":"MONEY","label_ru":"Сумма","label_en":"Total","fieldId":"total","isHidden":False}],
                "serviceEndpoint":{"account":{"user":{"id":"d822f440-d5c0-11ec-9d64-0242ac120002"},"id":"e2a32f7a-d5c0-11ec-9d64-0242ac120002"},"auth":{},"format":"XML","id":"2dccdb99-3721-45d9-8bd8-77d17f09c7dd","ip":"api.quickpay.kg","method":"POST","name":"Quickpay Service Endpoint","port":9202,"protocol":"HTTPS"}
            },
            "transactionId":trans_id,
            "userId":"ce85c750-fbee-4a0e-a5fa-dd33ced56b4f","bills":[],
            "sender":{"id":"ce85c750-fbee-4a0e-a5fa-dd33ced56b4f","account":{"id":"3a4e85cd-9a04-4fc4-8b77-3eea407f40f9","name":"ОАО \"ИнвесКор СА\""},"firstName":"ОАО","lastName":"ИнвесКор СА"},
            "userRole":"USER","amount":18,"fee":0,"net":18,
            "id":"3623332409_eb6fc7fb-cfb3-4a28-843b-57eb48599be1_CREDIT",
            "requestDate":1766569720317,"receiptNumber":"946427128545",
            "status":status,
            "statusCode":201
        }
        resp = requests.post(
            'http://127.0.0.1:8000/finik/webhook',
            headers={
                "Host": 'api.paymentsgateway.averspay.kg',  # matches what you signed
                "Content-Type": "application/json",
                "x-api-key": 'API_KEY',
                "x-api-timestamp": 'timestamp',
                "signature": 'signature123',
            },
            json=body1,
            allow_redirects=False,
        )

        print(f'🔥 target response {resp}')
        print(f'🔥 target response text {resp.text}')
        return Response({"Success": True})

class FinikRepaymentWebhookView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        #trans_id = request.data.get("transaction_id")
        trans_id = str(uuid.uuid4())
        status = request.data.get("status",default="SUCCEEDED")
        loan_id = request.data.get("loan_id")
        amount = request.data.get("amount",1)
        data = {
            'id': '320259584_2fea88ac-3a5c-4a29-abfa-9a07f1553bd3_DEBIT',
            'accountId': '3a4e85cd-9a04-4fc4-8b77-3eea407f40f9',
            'amount': amount,
            'clientId': '25c1aabe-fc4a-4968-85d9-90600466e9a5',
            'fields': {
                'amount': amount,
                'customer_id': 6,
                'loan_id':loan_id,
                'name': 'Disburse a loan',
                'qrTransactionId': trans_id
                },
            'receiptNumber': 173922807718,
            'requestDate': 1765184477058,
            'status': status,
            'transactionDate': 1765184509618,
            'transactionId': trans_id,
            'transactionType': 'DEBIT',
            'item': {'id': '1866399294_110ec58a-a0f6-4ac4-8353-c86cd813b8d1'}
            }
        resp = requests.post(
            'http://127.0.0.1:8000/payment/finik_repay/',
            headers={
                "Host": 'api.paymentsgateway.averspay.kg',  # matches what you signed
                "Content-Type": "application/json",
                "x-api-key": 'API_KEY',
                "x-api-timestamp": 'timestamp',
                "signature": 'signature123',
            },
            json=data,
            allow_redirects=False,
        )

        print(f'🔥 repay response {resp}')
        print(f'🔥 repay response text {resp.text}')
        return Response({"Success": True})
        

"""
finik extra_fee
{
    "id":"320259584_a6ff60a4-a008-4f9b-8dc0-d1ce168ce2b7_DEBIT",
    "accountId":"3a4e85cd-9a04-4fc4-8b77-3eea407f40f9",
    "amount":1,
    "clientId":"25c1aabe-fc4a-4968-85d9-90600466e9a5",
    "fields":{
        "amount":1,
        "approved":"true",
        "name":"",
        "customer_id":"73",
        "qrTransactionId":"a6ff60a4-a008-4f9b-8dc0-d1ce168ce2b7",
        "request_id":"151306ed-6a15-4d85-b1ca-352ba86b49db"
    },
    "receiptNumber":"330633310427",
    "requestDate":1768304218986,
    "status":"SUCCEEDED",
    "transactionDate":1768304221726,
    "transactionId":"a6ff60a4-a008-4f9b-8dc0-d1ce168ce2b7",
    "transactionType":"DEBIT",
    "item":{"id":"1866399294_2fa32970-c472-471e-9657-468636a9be60"}
}
"""
