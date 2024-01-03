import requests
import re

def turkish_id_verification(idnumber, name, lastname, birthyear):
    # return True
    url = "https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL"
    headers = {'Content-Type': 'text/xml; charset=utf-8'}
    body = """<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <TCKimlikNoDogrula xmlns="http://tckimlik.nvi.gov.tr/WS">
          <TCKimlikNo>%s</TCKimlikNo>
          <Ad>%s</Ad>
          <Soyad>%s</Soyad>
          <DogumYili>%s</DogumYili>
        </TCKimlikNoDogrula>
      </soap:Body>
    </soap:Envelope>""" % (idnumber, name, lastname, birthyear)
    # print(body)
    response = requests.post(url, data=body.encode('utf-8'), headers=headers)
    txt = response.content
    pattern = r"<TCKimlikNoDogrulaResult>(.*)<\/TCKimlikNoDogrulaResult>"
    x = re.findall(pattern, txt.decode('utf-8'))
    if x[0] == 'true':
        return True
    else:
        return False

print(turkish_id_verification('TCKIMLIK NO','ISIM','SOYISIM','DOGUMYILI'))
