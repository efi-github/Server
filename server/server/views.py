from django.http import HttpResponse

def respond_http(request,qr=""):
    if qr == "3fa06618-9aa8-41b5-a65e-a102f2309d88":
        return HttpResponse("{\r\n\"Type\": \"Mobile Phone\",\r\n\"Manufacturer\": \"Samsung\",\r\n\"Name\": \"Galaxy S7\",\r\n\"Deposit\": 20\r\n}", status=200)
    else:
        return HttpResponse('Does not exist',status=404)