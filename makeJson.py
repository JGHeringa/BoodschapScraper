from bs4 import BeautifulSoup
import requests
import time
import json
import pyperclip
from datetime import datetime

now = datetime.now()
datum = now.strftime("%d-%m-%Y %H:%M:%S")

#array with products
producten = []

# cat = ["aardappel-groente-fruit"]
cat = ["aardappel-groente-fruit", "salades-pizza-maaltijden", "vlees-kip-vis-vega", "kaas-vleeswaren-tapas", "zuivel-plantaardig-en-eieren", "bakkerij-en-banket", "ontbijtgranen-en-beleg", "snoep-koek-chips-en-chocolade", "tussendoortjes", "frisdrank-sappen-koffie-thee", "wijn-en-bubbels", "bier-en-aperitieven", "pasta-rijst-en-wereldkeuken", "soepen-sauzen-kruiden-olie", "sport-en-dieetvoeding", "diepvries", "drogisterij", "baby-en-kind", "huishouden", "huisdier"]

winkel = "Albert Heijn"
for catItem in cat:
    try:
        url = f"https://www.ah.nl/producten/{catItem}"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")

        page_text = doc.find(class_="typography_root__Om3Wh typography_variant-paragraph__T5ZAU load-more_paragraph__rV5-P")
        pages = int(str(page_text).split(">")[-2].split("de ")[-1].split(" resultaten")[-2])
        pageNr = pages // 31

        urlTotal = f"{url}?page={pageNr}"
        page = requests.get(urlTotal).text
        doc = BeautifulSoup(page, "html.parser")

        div = doc.find_all(class_="product-card-portrait_root__ZiRpZ product-grid-lane_gridItem__iTP0g")
        i = 0
        for item in div:
            naama = item.find(class_="line-clamp_root__7DevG line-clamp_active__5Qc2L title_lineclamp__kjrFA").string
            
            # filter character out
            naamb = naama.replace("'", "`")
            naamc = naamb.replace("ï", "i")
            naamd = naamc.replace("&", "en")
            naame = naamd.replace("à", "a")
            naamf = naame.replace("è", "e")
            naamg = naamf.replace("é", "e")
            naamh = naamg.replace("ê", "e")
            naami = naamh.replace("í", "i")
            naamj = naami.replace("ñ", "n")
            naamk = naamj.replace("ä", "a")
            naaml = naamk.replace("ü", "u")
            naamm = naaml.replace("â", "a")
            naamn = naamm.replace("ö", "o")
            naamo = naamn.replace("û", "u")
            naam = naamo.replace("ë", "e")
            prijsGroot = item.find(class_="price-amount_integer__+e2XO").string
            prijsKlein = item.find(class_="price-amount_fractional__kjJ7u").string
            perWat = item.find(class_="price_unitSize__Hk6E4").string
            prijs = float(prijsGroot + "." + prijsKlein)

            def makeDic():
                dict = {'naam': naam, 'prijs': prijs, 'perWat': perWat, 'catogorie': catItem, 'winkel': winkel}
                producten.append(dict)
            makeDic()
            i+=1
            print(i)
            if i == 40:
                # print(producten)
                productenJson = json.dumps(producten)
                url = 'http://boodschapcheck.nl/php/productScrap.php'
                data = f"producten={producten}&key=6346876345"
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                r = requests.post(url, data=data, headers=headers)
                if r.status_code == 200:
                    print("Successful request")
                else:
                    print(f"Request failed with status code: {r.status_code}")

                # Inspect the content of the response
                response_text = r.text
                print(response_text)
                i = 0
                producten = []
                time.sleep(0.1)

            
            # here was the request to php script to get it to the database
        time.sleep(1)
        
        productenJson = json.dumps(producten)
        pyperclip.copy(productenJson)
        url = ''#here url to php page to upload the data
        data = f"producten={producten}&key="
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        r = requests.post(url, data=data, headers=headers)

        if r.status_code == 200:
            print("Successful request")
        else:
            print(f"Request failed with status code: {r.status_code}")

        # Inspect the content of the response
        response_text = r.text
        print(response_text)
    except:
        pass