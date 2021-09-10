import qrcode

import json


def wishlist_makeqrs(wishlist):
    with open(wishlist) as json_file:
        data = json.load(json_file)
        for wish in data[0]:
            desc = wish["desc"]
            address = wish["address"]
            print(wish["address"])

            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )

            data = f"monero:{address}"

            qr.add_data(data)

            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img.save(f"{desc}.png")

wishlist_makeqrs("monerujo_wishlist.json")
