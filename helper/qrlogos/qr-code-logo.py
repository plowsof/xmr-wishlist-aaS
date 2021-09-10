import qrcode

import json

from PIL import Image


#Thrown together, so it's all hardcoded 

def wishlist_makeqrs(wishlist):
    with open(wishlist) as json_file:
        data = json.load(json_file)
        for wish in data[0]:
            desc = wish["desc"]
            address = wish["address"]
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
            img.save(f"{desc}.png")
            f_logo = "gunther2.png"
            logo = Image.open(f_logo)
            logo = logo.convert("RGBA")

            print(logo.size)
            im = Image.open(f"{desc}.png")
            im = im.convert("RGBA")
            logo.thumbnail((60, 60))


            #343 
            #region = logo
            #box = (135,135,235,235)
            #region = region.resize((box[2] - box[0], box[3] - box[1]))
            im.paste(logo, (142, 142))
            #im.show()
            im.save(f"{desc}.png")

wishlist_makeqrs("monerujo_wishlist.json")