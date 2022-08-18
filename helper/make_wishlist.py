
import pprint
import json
from datetime import datetime
import cryptocompare
import qrcode 
from PIL import Image
import requests
import os
import argparse
from github import Github
from monerorpc.authproxy import AuthServiceProxy, JSONRPCException
#Api key of "-" appears to work currently, this may change,
cryptocompare.cryptocompare._set_api_key_parameter("-")


git_username = "mj-xmr"
repo_name =  "wishlist-mj"
repo_dir = "json"
qrcode_dir = "qr_codes"
git_token = "" # Optional
rpc_user_default = 'monero'
prc_pass = 'mTC78KRoTzRm21amFYXoWA==|'
node_url_tpl =  'http://{0}:{1}@{2}:{3}/json_rpc'
json_url = f"https://raw.githubusercontent.com/{git_username}/{repo_name}/main/{repo_dir}/wishlist-data.json"
viewkey = "051b61127e35e8b539c070330443f431360edcc54089ee4b5f00f3b89e84270b"
main_address = "43yXPq28puShLkFcRgZ3kBXA2f7pmQFuweWDjt1GcKmuG5v9vRFUb81V3q8jwghxFg5bVRASKc4YedRmd3GJ9rxkBpdkGDM"
percent_buffer = 0.05

usd_goal_address = {}
wishes =[]

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u',  '--username',  default=rpc_user_default, type=str, help="RPC username shared via file in the working directory like: 'monero-wallet-rpc.18086.login'")
    parser.add_argument('-ps', '--password',       default='', type=str, help="RPC password shared via file in the working directory like: 'monero-wallet-rpc.18086.login'")
    parser.add_argument('-pf', '--password-file',  default='', type=str, help="RPC password file in the working directory like: 'monero-wallet-rpc.18086.login'")
    parser.add_argument('-p',  '--port',           default=18086, type=int, help="RPC wallet's port'")
    parser.add_argument('-ho', '--host',           default='localhost', type=str, help="RPC wallet's hostname'")

    return parser.parse_args()

def get_user_pass(args):
    if args.password_file:
        with open(args.password_file) as fin:
            pair = fin.read()
            return pair.split(':')
    password = prc_pass
    if args.password:
        password = args.password
    if args.username:
        return args.username, password

    return rpc_user_default, password

def get_node_url_args(args):
    rpc_user, rpc_pass = get_user_pass(args)
    return node_url_tpl.format(rpc_user, rpc_pass, args.host, args.port)

def getPrice(crypto,offset):
    data = cryptocompare.get_price(str(crypto), currency='USD', full=0)
    #print(f"[{crypto}]:{data[str(crypto)]['USD']}")
    value = float(data[str(crypto)]["USD"])
    #print(f"value = {value}")
    return(float(value) - (float(value) * float(offset)))

def formatAmount(amount):
    """decode cryptonote amount format to user friendly format.
    Based on C++ code:
    https://github.com/monero-project/bitmonero/blob/master/src/cryptonote_core/cryptonote_format_utils.cpp#L751
    """
    CRYPTONOTE_DISPLAY_DECIMAL_POINT = 12
    s = str(amount)
    if len(s) < CRYPTONOTE_DISPLAY_DECIMAL_POINT + 1:
        # add some trailing zeros, if needed, to have constant width
        s = '0' * (CRYPTONOTE_DISPLAY_DECIMAL_POINT + 1 - len(s)) + s
    idx = len(s) - CRYPTONOTE_DISPLAY_DECIMAL_POINT
    s = s[0:idx] + "." + s[idx:]

    #my own hack to remove trailing 0's, and to fix the 1.1e-5 etc
    trailing = 0
    while trailing == 0:
        if s[-1:] == "0":
            s = s[:-1]
        else:
            trailing = 1
    return s

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
    im.paste(logo,box=(142,142),mask=logo)
    #im.show()
    im.save(f"qrs/{title}.png")
    #uploadtogit(f"{title}.png",f"{title}.png")
    #return("lolok")

def wishlist_add_new(args, goal,desc,address,w_type):
    global git_username, repo_name, repo_dir, qrcode_dir
    global wishes
    global percent_buffer
    global usd_goal_address
    #global node_url
    #usd_goal_address.append(usd_address_pair)
    test = getPrice("XMR",float(percent_buffer))
    #print(f"test = {test}")
    xmrgoal = goal / getPrice("XMR",float(percent_buffer))
    

    #Connect and generate a new sub address for our wish
    if not address:
        print("Make a new address on the fly!")
        rpc_connection = AuthServiceProxy(service_url=get_node_url_args(args))
        #label could be added
        params={
                "account_index":0,
                "label": desc
                }
        info = rpc_connection.create_address(params)
        address = info["address"]
    usd_goal_address[address] = goal
    app_this = { 
                "goal":xmrgoal,
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
                "qr_img_url": f"https://raw.githubusercontent.com/{git_username}/{repo_name}/main/{qrcode_dir}/{address[0:12]}.png",
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
    #print("Before:")
    #pprint.pprint(current_wishlist)
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
    #uploadtogit("wishlist-data.json","wishlist-data.json")

#get input from a used wallet
def load_old_txs(args):
    global wishes
    rpc_connection = AuthServiceProxy(service_url=get_node_url_args(args))
    #label could be added
    params={
            "account_index":0,
            "in": True
            }
    old_txs = {}
    info = rpc_connection.get_transfers(params)
    num = 0

    if info["in"]:
        print("Wallet history detected. Importing")
        for tx in info["in"]:
            old_txs[num] = {tx["address"]: formatAmount(tx["amount"])}
            num += 1
        #pprint.pprint(old_txs)
        for wi in range(len(wishes)):
            for hi in range(len(old_txs)):
                #add, amount = old_txs[i]
                try:
                    if old_txs[hi][wishes[wi]["address"]]:
                        print(f"{wishes[wi]['address']} got +1 contributors and {old_txs[hi][wishes[wi]['address']]} XMR")
                        #pprint.pprint(wishes[wi])
                        wishes[wi]["contributors"] += 1
                        wishes[wi]["total"] += float(old_txs[hi][wishes[wi]["address"]])
                        wishes[wi]["percent"] = float(wishes[wi]["total"]) / float(wishes[wi]["goal"]) * 100  
                        #pprint.pprint(wishes[wi])
                except Exception as e:
                   continue
                

def create_new_wishlist(args):
    global wishes
    global viewkey, main_address

    #Your wishlist
    #-------------------------------------------------------------
    #wishlist_add_new(500,"Do something for the community",None,"work")
    #wishlist_add_new(5,"buy me a coffee (mdevs)","87UF7BP47y8Zins3C7ZHDWcUSgZBchtebguCaeRQiofyFT5L9PLhZ55EMC8e4WSHaLUzGYj5w5St2jQngCeHikaa4E36Dmv","gift")
    wishlist_add_new(args, 5,"buy me a coffee",'84N46mxVLM77YaqqMBzVe9cAN4ChBDjsXCvi9UtPVxdCeVeMfrJJM2kYv5ctp6V5taJUmRvhFWixfZ8iR2UySaRrDQgBPz7',"gift")
    #-------------------------------------------------------------
    
    thetime = datetime.now()
    total = {
        "total": 0,
        "contributors": 0,
        "modified": str(thetime),
        "title": "",
        "description": "",
        "image": "",
        "url": "",
        "viewkey": viewkey,
        "main_address": main_address
    }

    #search wallet for 'in' history, then compare addresses to our new list.
    #if matching address are found then contributors are +=1'd and amount+=amount.
    load_old_txs(args)

    the_wishlist = {}
    the_wishlist["wishlist"] = wishes
    the_wishlist["metadata"] = total


    with open("wishlist-data.json", "w+") as f:
        json.dump(the_wishlist,f, indent=4)

    #Original xmr goal + address pairings
    with open("usd-address-pair.json", "w+") as f:
        json.dump(usd_goal_address,f,indent=4)
    

    return 
'''
//-----------------------------
// What / Why
//-----------------------------

calling create_new_wishlist will do several things:
    - convert the usd value to xmr with a buffer (percent_buffer)
    - create a new address for the wish if 'None' is supplied
    - generate QRimages, and adds a qr_img_url to the json - which expects you to place them in your 'qrimage_dir' @ github
    - creates 2 file:
        - wishlist-data.json file to uploaded to github (manually)
        - usd-address-pair.json which is just a list of your addresses + original usd goal which is later used by adjust_goals()
    - load_old_txs() will get / import old tx's that have a matching address to those in your wishlist (++contributors/amounts) 

You can manually adjust the json after the fact by hand or using an online json editor (easier)

Why github?'
- it's free, and you can also host a website on github pages.
- Did i mention its free? 
- Extra accountability as its a public ledger - edits to the json data/qr images are logged
- See Monerujo's adaptation if you want to self host everything.

//-----------------------------
// How
//-----------------------------

go to create_new_wishlist() and add each of your wishes using a USD goal amount.
Supply None as the address if you want to make a new one (has to be connected to an rpc wallet)

'''

args = get_args()
create_new_wishlist(args)

#Recalculate goals based on current USD value (with a buffer also) amd upload new data
#adjust_goals(0.20)

#change_all_titles("XMR.radio donation")

