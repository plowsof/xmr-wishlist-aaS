

import pprint
import json
from datetime import datetime
import cryptocompare
import qrcode 
from PIL import Image
import requests
import os
from github import Github

git_username = "plowsof"

repo_name =  "funding-xmr-radio"
repo_dir = "json"
git_token = "hunter123secret"
cryptocompare.cryptocompare._set_api_key_parameter("-")
wishes =[]
percent_buffer = 0.05
json_url = "https://raw.githubusercontent.com/plowsof/funding-xmr-radio/main/json/wishlist-data.json"
usd_goal_address = {}

def getPrice(crypto,offset):
    data = cryptocompare.get_price(str(crypto), currency='USD', full=0)
    print(f"[{crypto}]:{data[str(crypto)]['USD']}")
    value = float(data[str(crypto)]["USD"])
    print(f"value = {value}")
    return(float(value) - (float(value) * float(offset)))

def put_qr_code(address):
    try:
        if not os.path.isdir(os.path.join('.','qrs')):
            os.mkdir(os.path.join(".","qrs"))
        pass
    except Exception as e:
        raise e

    title = address[0:12]
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=7,
        border=4,
    )

    data = f"monero:{address}"

    qr.add_data(data)

    qr.make(fit=True)

    #img = qr.make_image(fill_color="black", back_color=(62,62,62))
    img = qr.make_image(fill_color=(62,62,62), back_color="white")
    img.save(f"qrs/{title}.png")
    f_logo = os.path.join(".","qrs","logo3.png")
    logo = Image.open(f_logo)
    logo = logo.convert("RGBA")

    print(logo.size)
    im = Image.open(f"qrs/{title}.png")
    im = im.convert("RGBA")
    logo.thumbnail((60, 60))

    #im.paste(logo, (142, 142))
    #Image.alpha_composite(im, logo).show() #.save("test3.png")
    im.paste(logo,box=(142,142),mask=logo)
    #im.show()
    im.save(f"qrs/{title}.png")
    #uploadtogit(f"{title}.png",f"{title}.png")
    #return("lolok")


def wishlist_add_new(goal,desc,address,w_type):
    global git_username
    global repo_name
    global repo_dir
    global wishes
    global percent_buffer
    global usd_goal_address
    usd_goal_address[address] = goal
    #usd_goal_address.append(usd_address_pair)
    test = getPrice("XMR",float(percent_buffer))
    print(f"test = {test}")
    goal = goal / getPrice("XMR",float(percent_buffer))
    app_this = { 
                "goal":goal,
                "total":0,
                "contributors":0,
                "address":address,
                "description": desc,
                "percent": 0,
                "type": w_type,
                "created_date": str(datetime.now()),
                "modified_date": str(datetime.now()),
                "author_name": "",
                "author_email": "",
                "id": address[0:12],
                "qr_img_url": f"https://raw.githubusercontent.com/{git_username}/{repo_name}/main/{repo_dir}/{address[0:12]}.png",
                "title": ""
    } 
    wishes.append(app_this)
    put_qr_code(address)

def getJson():
    #must get the latest json as it may have been changed
    global json_url
    try:
        x = requests.get(json_url)
        return json.loads(x.text)
    except Exception as e:
        raise e

#Re-make goals using the current USD value of XMR + % buffer
def adjust_goals(new_buffer):
    #get Json
    current_wishlist = getJson()
    print("Before:")
    pprint.pprint(current_wishlist)
    #we need the usd amount + address to do this
    with open("usd-address-pair.json") as f:
        usd_pairings = json.load(f)
    #Adjust all goals
    for wish in current_wishlist["wishlist"]:
        if usd_pairings[wish["address"]]:
            #we exist
            usd_xmr = getPrice("XMR",float(new_buffer))
            new_goal = usd_pairings[wish["address"]] / usd_xmr
            old_goal = wish["goal"]
            print(f"old goal was:{old_goal} new goal: {new_goal}")
            wish["goal"] = new_goal
            wish["percent"] = float(wish["total"]) / float(wish["goal"]) * 100 
    #Send back to github with only goals/percent adjusted
    #Set modified time to JS reloads our new info
    current_wishlist["metadata"]["modified"] = str(datetime.now())
    dump_json(current_wishlist)
    #upload to git
    #uploadtogit("wishlist-data.json","wishlist-data.json")

def dump_json(wishlist):    
    with open('wishlist-data.json', 'w') as f:
        json.dump(wishlist, f, indent=6)  

def uploadtogit(infile,outfile):
    global repo_name 
    global repo_dir
    global git_token
    g = Github(git_token)

    repo = g.get_user().get_repo(repo_name)

    with open(infile, 'r') as file:
        content = file.read()
    #print(outfile)
    # Upload to github
    git_file = repo_dir + "/" + outfile
    contents = repo.get_contents(git_file)
    repo.update_file(contents.path, "committing files", content, contents.sha, branch="main")
    print(git_file + ' UPDATED')

def change_all_titles(title):
    now_list = getJson()
    for wish in now_list["wishlist"]:
        wish["title"] = title
    #Set modified time to JS re-loads new info
    now_list["metadata"]["modified"] = str(datetime.now())
    dump_json(now_list)
    #Check that the .json file is 'sane', or live life in the fast lane:
    uploadtogit("wishlist-data.json","wishlist-data.json")



def create_new_wishlist():

    wishlist_add_new(180,"Mixcloud Pro annual subscription (2021-2022)","8B98rGurDboU2XvfrqFJuA84E3U9J2f2cZPi63Cjnq9uec92V7J3NqRJHqA7h3i3K5Lh3fE7ZTxeRc6hk4UyovcmUdvobG3", "subs")
    wishlist_add_new(270,"XMR.radio domain renewal (2022-2023)","86xE6BVX3c32o6jtEHAsvd43qSr1Jzn1Jcr4hCdHkB9dgMCLg1ZpGvaNKbuhkf4E98UWFcag5m92oBLWQiqQbJvYEw4r9Af","subs")
    wishlist_add_new(48,"ProtonMail Plus renewal (2022-2023)","87LxtQdft3658BogUHXekShCLzbeueL2P1H3dw3h824yMsvPXdbnYBcCphvbhiVu33HNnFGx7nU7eFEMbMpRU6eWNw5pRC5","subs")
    wishlist_add_new(240,"OVH US VPS annual (2022-2023)","85Dw6FurwyFgPbnsnW4v3cUTVeAkkvEw2jHvvaJ5PiyRGVvp4GcHyAQ71YTVC6637AMjrcP8yKdcoCHosWNEY1hz3HUXBeZ","subs") #16
    wishlist_add_new(1500,"Music acquisition budget (2022-2023)","8Bxyj1J5KfVWLxZcrH7kjtNRTAmCSLFRZiJpxp5RtZRz9YFGyhUEwwZPucPGHaYVKsYBCCtiPRy6BMyUL5soGd9KFfnmKFn","subs")

    #Equipment / Peripherals 
    wishlist_add_new(457,"Rode Wireless GO II 2-Person Lavalier Microphone System/Recorder Kit","85vWUxkpPSw2awQrouD5mkVLyG6voEMQpdD8KZM3TVfPSriBWhX7Au4cdHHgaDQx4bQJoQXgpijtDaLshqLbNjcsN6Vzba9","equip")
    wishlist_add_new(20,"Rode Wireless GO Case","89yR6wHYngjgxvMXubZjbd8g7kt3iocThZaQ9vDx74iG2d2aBCBnjSeDCaGKMpZ1SSdNY4TAyF9bZ8siHm3UGL9K62mMfpZ","equip")
    wishlist_add_new(13,"TRS to XLR breakout cable, 3.3 feet","86K8gZC2roNAiVZ9boVWQVUX2bU6KCecAbBM1rhpLZGHHtBQUChukoXXP3SWjaYSsCgCUGaFvwAjkJZAhPeZK88zN46msfz","equip")

    wishlist_add_new(29,"Rode Interview GO Handheld Mic Adapter for the Wireless GO","86AJAxavmaL2hvowhGs5gHGkLDGHoBgUYGGacSDuHGE1Si14KqHbyfx1YqzkfS2h3E4n5QefQtd7S4g9YxovPfaXHKdLMVe","equip")
    wishlist_add_new(150,"Audio-Technica ATH-M50X","8AP95vZNoog7jEmRzmRMxmR8aAa1uFH3oiMaczjo7KYXKNTceBQkRNxLuXKicN61Wgf28TFzcgmbFRfjKm6VLbNx2BLpV5t","equip")
    wishlist_add_new(15,"Audio-Technica Case","84QzYrxCxHJ4r6sRyqE6HVi8ZGxvVCDxhK4YkYm3Khi5imcCGxozDADeo6KxsPKRC2W8HD9ei2QPh81vyzBn1iPkTWaVf89","equip")

    wishlist_add_new(170,"Focusrite Scarlett 2i2 2x2 USB Audio Interface (3rd Gen)","83RNVysW2M1jPyVSzYJmWRDSQQmAH2aHHhBtoLis7X2nYA6dq752Z9K7vtDkcSgpaxddvc7Jj62rPTMebeNz4jhi4NPzB25","equip")
    wishlist_add_new(16,"Focusrite Scarlett case","89kmrkP9ig1B1rvL4pnXJXNcFX9TcUtjLFcsxF88b7fKfE8zr2WfitL3znkqzoxowFUHgWyQusFmoDpn91kf5LezUJrJgri","equip")

    wishlist_add_new(250,"Samsung 2TB T5 Portable SSD","86VTYd17e4y4V79c82GWb8jSWz1K2tD3BSPAJhHrjAwYaQNkq8wsQw7PAsyWT2zPBZa3s4B8t5K8Y1ntJCWYUw5i2Ji33ig","equip")
    wishlist_add_new(10,"Samsung T5 Case","86y4QiHDJv7jHj9LxYGLKt6kn5Uq9vfq8jRkKVFLNq6X5Ma6kBhmaoAWaQgGVebq3C25MyezwhDn3AaXrJRgFL11DjMDWWF","equip")

    thetime = datetime.now()
    total = {
        "total": 0,
        "contributors": 0,
        "modified": str(thetime),
        "title": "",
        "description": "",
        "image": "",
        "url": ""
    }

    the_wishlist = {}
    the_wishlist["wishlist"] = wishes
    the_wishlist["metadata"] = total


    with open("wishlist-data.json", "w+") as f:
        json.dump(the_wishlist,f, indent=4)


    with open("usd-address-pair.json", "w+") as f:
        json.dump(usd_goal_address,f,indent=4)
    #dump address + usd goal pairings



create_new_wishlist()

#Recalculate goals based on current USD value (with a buffer also) amd upload new data
#Assumes your json data is old/modified and is being remotely stored on github
#adjust_goals(0.20)

#change_all_titles("XMR.radio donation")
