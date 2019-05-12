from django.http import HttpResponse

def respond_http(request,qr=""):
    if qr == "nas80dtw3ß28zasd0na0":
        return HttpResponse('Mobile Phone - Samsung - Galaxy S7 - 20€',status=200)
    else:
        return HttpResponse('Does not exist',status=404)