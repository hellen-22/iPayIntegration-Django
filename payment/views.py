import random
import hashlib
import hmac

from urllib.parse import urlparse, parse_qs
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse


def random_strings(length_of_string):
    str_result = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(str_result) for _ in range(length_of_string))

def payment_form(request):
    generated_hash = ""
    fields = {}

    if request.method == 'POST' and 'pay_btn' in request.POST:
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        amount = "1"

        fields = {
            "live": "1",
            "oid": random_strings(6),
            "inv": "123456789",
            "ttl": amount,
            "tel": phone_number,
            "eml": email,
            "vid": "demo",
            "curr": "KE",
            "p1": '',
            "p2": "",
            "p3": "",
            "p4": "",
            "cbk": request.build_absolute_uri(reverse('check')),
            "cst": "1",
            "crl": "2",
        }

        datastring = fields['live'] + fields['oid'] + fields['inv'] + fields['ttl'] + fields['tel'] + fields['eml'] + fields['vid'] + fields['curr'] + fields['p1'] + fields['p2'] + fields['p3'] + fields['p4'] + fields['cbk'] + fields['cst'] + fields['crl']
        hashkey = "demoCHANGED"
        
        hashkey = hashkey.encode('utf-8')
        datastring = datastring.encode('utf-8')

        # Compute the HMAC-SHA1 hash
        generated_hash = hmac.new(hashkey, datastring, hashlib.sha1).hexdigest()

        redirect_url = f"https://payments.ipayafrica.com/v3/ke?live={fields['live']}&oid={fields['oid']}&inv={fields['inv']}&ttl={fields['ttl']}&tel={fields['tel']}&eml={fields['eml']}&vid={fields['vid']}&curr={fields['curr']}&p1={fields['p1']}&p2={fields['p2']}&p3={fields['p3']}&p4={fields['p4']}&cbk={fields['cbk']}&cst={fields['cst']}&crl={fields['crl']}&hsh={generated_hash}"
        return redirect(redirect_url)

    return render(request, 'payment_form.html')


def checkpayment(request):
    parsed_url = urlparse(request.build_absolute_uri())
    query_params = parse_qs(parsed_url.query)
    status = query_params.get('status')

    print(status)

    return HttpResponse("Successful")