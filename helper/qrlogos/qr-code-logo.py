import qrcode

import json
import requests
from PIL import Image


json_url = "https://funding.monerujo.app/wishlist-data.json"

#Thrown together, so it's all hardcoded 

def getJson():
    global json_url
    x = requests.get(json_url)
    return json.loads(x.text)


def wishlist_makeqrs():
    saved_wishlist = getJson()
    for wish in saved_wishlist[0]:
        desc = wish["desc"]
        address = wish["address"]
        title = wish["title"]
        print(wish["address"])

        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=7,
            border=4,
        )

        data = f"monero:{address}"

        qr.add_data(data)

        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(f"{title}.png")
        f_logo = "gunther2.png"
        logo = Image.open(f_logo)
        logo = logo.convert("RGBA")

        print(logo.size)
        im = Image.open(f"{title}.png")
        im = im.convert("RGBA")
        logo.thumbnail((60, 60))

        im.paste(logo, (142, 142))
        #im.show()
        im.save(f"{title}.png")

wishlist_makeqrs()