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
        payload = request.data  # Gets full POST payload as dict
        print(f'🔥 payload {payload}')
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
        #return Response({"Success":False})
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

class OdinesCreditLimitView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        return Response({"Success": True, "ErrorList": None, "ErrorDescription": "","Result":{"approved":True,"limit":30000,"score":202}})
    
class OdinesCustomerView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        return Response({"Success": True, "ErrorList": None, "ErrorDescription": "","Result":{"isFound":True,"customerGuid": "2a37a3b4-c47b-11ed-bba9-00155d056d37"}})
    
class OdinesSelfBlockView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        return Response({"Success": True, "ErrorList": None, "ErrorDescription": "","Result":{"is_selfblocked_ishenim":False,"is_selfblocked_sns": False}})
    
    
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
class TundukXMLView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        #bankpin
        raw_xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<SOAP-ENV:Envelope xmlns:SOAP-ENV=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:id=\"http://x-road.eu/xsd/identifiers\" xmlns:xrd=\"http://x-road.eu/xsd/xroad.xsd\"><SOAP-ENV:Header><xrd:client id:objectType=\"SUBSYSTEM\"><id:xRoadInstance>central-server</id:xRoadInstance><id:memberClass>COM</id:memberClass><id:memberCode>60000048</id:memberCode><id:subsystemCode>cbs-system2</id:subsystemCode></xrd:client><xrd:service id:objectType=\"SERVICE\"><id:xRoadInstance>central-server</id:xRoadInstance><id:memberClass>GOV</id:memberClass><id:memberCode>70000005</id:memberCode><id:subsystemCode>passport-service</id:subsystemCode><id:serviceCode>bankPinService</id:serviceCode><id:serviceVersion>v1</id:serviceVersion></xrd:service><xrd:userId>zolotoi_main_adapter</xrd:userId><xrd:id>ed664512a222</xrd:id><xrd:requestHash algorithmId=\"http://www.w3.org/2001/04/xmlenc#sha512\">YEkb1WA65JtJPKSVLv5+puaqm3JUmlvjZa0867dTZSXn1jUNSs1mjTa7UrK9xgdC4384oUtb5jyLFPk8ioK/FQ==</xrd:requestHash><xrd:issue>django-bankpin</xrd:issue><xrd:protocolVersion>4.0</xrd:protocolVersion></SOAP-ENV:Header><SOAP-ENV:Body><ts1:bankPinServiceResponse xmlns:ts1=\"http://tunduk-seccurity-infocom.x-road.fi/producer\"><ts1:request>\n            <ts1:clientid>mkk_gold_standard</ts1:clientid>\n            <ts1:secret>bwrXn7gibNvQ2aXA9iK2</ts1:secret>\n            <ts1:pin>20104198601570</ts1:pin>\n            <ts1:series>ID</ts1:series>\n            <ts1:number>3739529</ts1:number>\n         </ts1:request><ts1:response><ts1:pin>20104198601570</ts1:pin><ts1:surname>НУРАДИЛ УУЛУ</ts1:surname><ts1:name>ТЕМИРБЕК</ts1:name><ts1:patronymic></ts1:patronymic><ts1:familyStatus>1</ts1:familyStatus><ts1:maritalStatus></ts1:maritalStatus><ts1:gender>M</ts1:gender><ts1:dateOfBirth>1986-04-01T00:00:00</ts1:dateOfBirth><ts1:passportSeries>ID</ts1:passportSeries><ts1:passportNumber>3739529</ts1:passportNumber><ts1:voidStatus>0</ts1:voidStatus><ts1:issuedDate>2024-01-08T00:00:00</ts1:issuedDate><ts1:passportAuthority>МРО 01-03 ПЕРВОМАЙСКИЙ Р-Н</ts1:passportAuthority><ts1:passportAuthorityCode>211031</ts1:passportAuthorityCode><ts1:expiredDate>2034-01-08T00:00:00</ts1:expiredDate><ts1:message>Кыргызская Республика,Чуйская обл.,Московский р-н,Нарзан а/а,с. Беловодское, улица Октябрьская, дом 116</ts1:message><ts1:addressRegion>ЧҮЙ ОБЛ.,МОСКВА Р-НУ</ts1:addressRegion><ts1:addressLocality>БЕЛОВОДСКОЕ А.</ts1:addressLocality><ts1:addressStreet>ОКТЯБРЬСКАЯ КӨЧ.</ts1:addressStreet><ts1:addressHouse>116</ts1:addressHouse><ts1:addressBuilding></ts1:addressBuilding><ts1:addressApartment></ts1:addressApartment><ts1:addressArray><ts1:countryId>4948</ts1:countryId><ts1:regionId>6940</ts1:regionId><ts1:districtId>7189</ts1:districtId><ts1:aymakId>7205</ts1:aymakId><ts1:villageId>7206</ts1:villageId><ts1:streetId>26291</ts1:streetId><ts1:houseId>740861</ts1:houseId><ts1:houseTxt>116</ts1:houseTxt><ts1:flatId>0</ts1:flatId><ts1:flatTxt></ts1:flatTxt><ts1:code>7060400070407</ts1:code><ts1:post></ts1:post></ts1:addressArray><ts1:photo>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</ts1:photo></ts1:response></ts1:bankPinServiceResponse></SOAP-ENV:Body></SOAP-ENV:Envelope>"
        
        return HttpResponse(raw_xml, content_type="application/xml; charset=utf-8", status=200)
    

class TundukBankpinView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        return Response({
        "ok": True,
        "http_status": 200,
        "response": {
            "ok": True,
            "data": {
                "response": {
                    "pin": "20104198601570",
                    "surname": "НУРАДИЛ УУЛУ",
                    "name": "ТЕМИРБЕК",
                    "patronymic": {},
                    "familyStatus": "1",
                    "maritalStatus": {},
                    "gender": "M",
                    "dateOfBirth": "1986-04-01T00:00:00",
                    "passportSeries": "ID",
                    "passportNumber": "3739529",
                    "voidStatus": "0",
                    "issuedDate": "2024-01-08T00:00:00",
                    "passportAuthority": "МРО 01-03 ПЕРВОМАЙСКИЙ Р-Н",
                    "passportAuthorityCode": "211031",
                    "expiredDate": "2034-01-08T00:00:00",
                    "message": "Кыргызская Республика,Чуйская обл.,Московский р-н,Нарзан а/а,с. Беловодское, улица Октябрьская, дом 116",
                    "addressRegion": "ЧҮЙ ОБЛ.,МОСКВА Р-НУ",
                    "addressLocality": "БЕЛОВОДСКОЕ А.",
                    "addressStreet": "ОКТЯБРЬСКАЯ КӨЧ.",
                    "addressHouse": "116",
                    "addressBuilding": {},
                    "addressApartment": {},
                    "addressArray": {
                        "countryId": "4948",
                        "regionId": "6940",
                        "districtId": "7189",
                        "aymakId": "7205",
                        "villageId": "7206",
                        "streetId": "26291",
                        "houseId": "740861",
                        "houseTxt": "116",
                        "flatId": "0",
                        "flatTxt": {},
                        "code": "7060400070407",
                        "post": {}
                    },
                    "photo": "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"
                }
            }
        },
        "raw_xml": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<SOAP-ENV:Envelope xmlns:SOAP-ENV=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:id=\"http://x-road.eu/xsd/identifiers\" xmlns:xrd=\"http://x-road.eu/xsd/xroad.xsd\"><SOAP-ENV:Header><xrd:client id:objectType=\"SUBSYSTEM\"><id:xRoadInstance>central-server</id:xRoadInstance><id:memberClass>COM</id:memberClass><id:memberCode>60000048</id:memberCode><id:subsystemCode>cbs-system2</id:subsystemCode></xrd:client><xrd:service id:objectType=\"SERVICE\"><id:xRoadInstance>central-server</id:xRoadInstance><id:memberClass>GOV</id:memberClass><id:memberCode>70000005</id:memberCode><id:subsystemCode>passport-service</id:subsystemCode><id:serviceCode>bankPinService</id:serviceCode><id:serviceVersion>v1</id:serviceVersion></xrd:service><xrd:userId>zolotoi_main_adapter</xrd:userId><xrd:id>ed664512a222</xrd:id><xrd:requestHash algorithmId=\"http://www.w3.org/2001/04/xmlenc#sha512\">YEkb1WA65JtJPKSVLv5+puaqm3JUmlvjZa0867dTZSXn1jUNSs1mjTa7UrK9xgdC4384oUtb5jyLFPk8ioK/FQ==</xrd:requestHash><xrd:issue>django-bankpin</xrd:issue><xrd:protocolVersion>4.0</xrd:protocolVersion></SOAP-ENV:Header><SOAP-ENV:Body><ts1:bankPinServiceResponse xmlns:ts1=\"http://tunduk-seccurity-infocom.x-road.fi/producer\"><ts1:request>\n            <ts1:clientid>mkk_gold_standard</ts1:clientid>\n            <ts1:secret>bwrXn7gibNvQ2aXA9iK2</ts1:secret>\n            <ts1:pin>20104198601570</ts1:pin>\n            <ts1:series>ID</ts1:series>\n            <ts1:number>3739529</ts1:number>\n         </ts1:request><ts1:response><ts1:pin>20104198601570</ts1:pin><ts1:surname>НУРАДИЛ УУЛУ</ts1:surname><ts1:name>ТЕМИРБЕК</ts1:name><ts1:patronymic></ts1:patronymic><ts1:familyStatus>1</ts1:familyStatus><ts1:maritalStatus></ts1:maritalStatus><ts1:gender>M</ts1:gender><ts1:dateOfBirth>1986-04-01T00:00:00</ts1:dateOfBirth><ts1:passportSeries>ID</ts1:passportSeries><ts1:passportNumber>3739529</ts1:passportNumber><ts1:voidStatus>0</ts1:voidStatus><ts1:issuedDate>2024-01-08T00:00:00</ts1:issuedDate><ts1:passportAuthority>МРО 01-03 ПЕРВОМАЙСКИЙ Р-Н</ts1:passportAuthority><ts1:passportAuthorityCode>211031</ts1:passportAuthorityCode><ts1:expiredDate>2034-01-08T00:00:00</ts1:expiredDate><ts1:message>Кыргызская Республика,Чуйская обл.,Московский р-н,Нарзан а/а,с. Беловодское, улица Октябрьская, дом 116</ts1:message><ts1:addressRegion>ЧҮЙ ОБЛ.,МОСКВА Р-НУ</ts1:addressRegion><ts1:addressLocality>БЕЛОВОДСКОЕ А.</ts1:addressLocality><ts1:addressStreet>ОКТЯБРЬСКАЯ КӨЧ.</ts1:addressStreet><ts1:addressHouse>116</ts1:addressHouse><ts1:addressBuilding></ts1:addressBuilding><ts1:addressApartment></ts1:addressApartment><ts1:addressArray><ts1:countryId>4948</ts1:countryId><ts1:regionId>6940</ts1:regionId><ts1:districtId>7189</ts1:districtId><ts1:aymakId>7205</ts1:aymakId><ts1:villageId>7206</ts1:villageId><ts1:streetId>26291</ts1:streetId><ts1:houseId>740861</ts1:houseId><ts1:houseTxt>116</ts1:houseTxt><ts1:flatId>0</ts1:flatId><ts1:flatTxt></ts1:flatTxt><ts1:code>7060400070407</ts1:code><ts1:post></ts1:post></ts1:addressArray><ts1:photo>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</ts1:photo></ts1:response></ts1:bankPinServiceResponse></SOAP-ENV:Body></SOAP-ENV:Envelope>\n"
    })

class TundukSocfundPermissionCheckView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        return Response({
            "ok": True,
            "http_status": 200,
            "permissions": [
                {
                    "id": "c689b4b9-a988-43e2-9a60-71f02cf24aae",
                    "status": "Accepted",
                    "pin": "20104198601570",
                    "last_name": "Нурадил уулу",
                    "first_name": "Темирбек",
                    "patronymic": None,
                    "phone_number": "+996553000665",
                    "organization_name": "ОАО \"МФК \"ИнвесКор СА\"",
                    "inn": "02301200410114",
                    "bic": "023012",
                    "request_date": "2025-11-17T09:54:51.4915688"
                },
                {
                    "id": "8c54ad4e-dfc8-4a84-b59d-2fea636c3c7a",
                    "status": "Accepted",
                    "pin": "20104198601570",
                    "last_name": "Нурадил уулу",
                    "first_name": "Темирбек",
                    "patronymic": None,
                    "phone_number": "+996553000665",
                    "organization_name": "ОАО \"МФК \"ИнвесКор СА\"",
                    "inn": "02301200410114",
                    "bic": "023012",
                    "request_date": "2025-10-29T06:44:21.1342105"
                },
                {
                    "id": "f26664bc-dbc7-48d1-b388-0a6ba8fd24dd",
                    "status": "Accepted",
                    "pin": "20104198601570",
                    "last_name": "Нурадил уулу",
                    "first_name": "Темирбек",
                    "patronymic": None,
                    "phone_number": "+996553000665",
                    "organization_name": "ОАО \"МФК \"ИнвесКор СА\"",
                    "inn": "02301200410114",
                    "bic": "023012",
                    "request_date": "2025-10-28T09:29:04.7740572"
                }
            ],
            "raw_xml":""
        })
    
class TundukSocfundPermissionInitView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        return Response({
            "ok": True,
            "http_status": 200,
            "response": {
                "operation_result": True,
                "message": "На мобильный телефон застрахованного лица был отправлен код для идентификации",
                "request_id": "8c54ad4e-dfc8-4a84-b59d-2fea636c3c7a",
                "otp_required": True
            },
            "raw_xml":""
        })
    
class TundukSocfundPermissionConfirmView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        return Response({
            "ok": True,
            "http_status": 200,
            "response": {
                "operation_result": True,
                "message": "Выдано разрешение для получения персональных данных застрахованного лица с 17.11.2025 по 18.12.2025",
                "permission_id": "c689b4b9-a988-43e2-9a60-71f02cf24aae"
            },
            "raw_xml": ""
        })
    
class TundukCheckView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        return Response({
        "ok": True,
        "results": []
    })
    def get(self, request):
        return Response({
        "ok": True,
        "results": []
    })
    
    

class TundukWorkPeriodViewView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        return Response({
            "ok": True,
            "raw": "",
            "data": {
                "OperationResult": "true",
                "WorkPeriodInfo": {
                    "State": "OK",
                    "PIN": "20104198601570",
                    "FirstName": "Темирбек",
                    "LastName": "Нурадил уулу",
                    "Patronymic": {},
                    "Issuer": "Социальный фонд Кыргызской Республики",
                    "WorkPeriods": {
                        "WorkPeriodWithSumDto": [
                            {
                                "PIN_LSS": "20104198601570",
                                "Payer": "ОсОО \"ПроСофт\"         (ПВТ с мая месяца)",
                                "INN": "02402201110081",
                                "NumSF": "101000751182",
                                "DateBegin": "01.01.2022",
                                "DateEnd": "31.01.2022",
                                "Salary": "22677.00"
                            },]}}}
        })
