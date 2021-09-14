import pprint
from datetime import datetime
import pickle
import time
import os
import sys
import random
import json
import requests
from github import Github
from monerorpc.authproxy import AuthServiceProxy, JSONRPCException
#from matrix_client.api import MatrixHttpApi
#import emoji
from filelock import FileLock


os.chdir("/home/your/scripts/dir")

wishlist = []
repo_name =  "funding-xmr-radio"
repo_dir = "json"
node_url =  'http://eeebox:18086/json_rpc'
#node_url = 'http://localhost:18082/json_rpc'
git_token = "ghp_hunter2********"
json_url = "https://raw.githubusercontent.com/plowsof/funding-xmr-radio/main/json/wishlist-data.json"
matrix_token = "-"
matrix_room = "-"

def getJson():
    #must get the latest json as it may have been changed
    global json_url
    try:
        x = requests.get(json_url)
        return json.loads(x.text)
    except Exception as e:
        raise e

def main(tx_id,conf=0,multi=0):
    #check height
    saved_wishlist = getJson()
    if multi == 0:
        tx_data = checkHeight(tx_id,conf)
        if tx_data:
            print(tx_data["address"])
    else:
        tx_data = tx_id
    if tx_data:
        #print(f"we got funds : {tx_data['address']}")
        tx_data["amount"] = formatAmount(tx_data["amount"])
        found = 0
        main_fund = saved_wishlist["metadata"]["total"]
        for i in range(len(saved_wishlist["wishlist"])):
            try:
                #print(saved_wishlist[i])
                if saved_wishlist["wishlist"][i]["address"] == tx_data["address"]:
                    found = 1
                    saved_wishlist["wishlist"][i]["modified_date"] = str(datetime.now())
                    #contributor += 1 
                    saved_wishlist["wishlist"][i]["contributors"] += 1
                    #total += amount
                    saved_wishlist["wishlist"][i]["total"] += float(tx_data["amount"])
                    #print(f"after:{saved_wishlist["wishlist"][i]")
                    #if total => goal its 100%
                    if float(saved_wishlist["wishlist"][i]["total"]) >= float(saved_wishlist["wishlist"][i]["goal"]):
                        #fully funded [ do something special e.g. make a tweet ...]
                        if saved_wishlist["wishlist"][i]["percent"] != 100:
                            #We are newly fully funded
                            print("something special")
                            #matrixMsg(saved_wishlist["wishlist"][i])
                        saved_wishlist["wishlist"][i]["percent"] = 100
                    else:
                        saved_wishlist["wishlist"][i]["percent"] = float(saved_wishlist["wishlist"][i]["total"]) / float(saved_wishlist["wishlist"][i]["goal"]) * 100         
                    break
            except Exception as e:
                raise e
        if found == 0:
            extra_xmr = tx_data["amount"]
            #donation received on invalid wishlist
            saved_wishlist["metadata"]["total"] += float(extra_xmr)
            saved_wishlist["metadata"]["contributors"] += 1

        #finished. unless "batched" doesn't exist
        saved_wishlist["wishlist"] = sorted(saved_wishlist["wishlist"], key=lambda k: k['percent'],reverse=True)
        modified = str(datetime.now())
        saved_wishlist["metadata"]["modified"] = modified
        print(modified)
        #pickle.dump(saved_wishlist, open( "wishlist.p", "wb+" ) )
        dump_json(saved_wishlist)
        if not os.path.isfile("batched"):
            #create "batched"
            with open("batched", "w+") as f:
                f.write("1")
            time.sleep(30)
            uploadtogit("wishlist-data.json","wishlist-data.json")
            os.remove("batched")

def dump_json(wishlist):
    with FileLock("wishlist-data.json.lock"):
        print("Lock acquired.")
        with open('wishlist-data.json', 'w') as f:
            json.dump(wishlist, f, indent=6)  

def matrixMsg(data):
    global matrix_token
    global matrix_room
    message = data["desc"] + emoji.emojize(' is 100% FUNDED @twisted_turtle :thumbs_up:')
    matrix = MatrixHttpApi("https://matrix.org", token=matrix_token)
    response = matrix.send_message(matrix_room, message)

def checkHeight(tx_id,conf=0):
    global pickled_data
    global node_url
    #loop incase rpc daemon has not started up yet.
    while True:
        try:
            rpc_connection = AuthServiceProxy(service_url=node_url)
            params={"account_index":0,
            "txid":str(tx_id)}
            info = rpc_connection.get_transfer_by_txid(params)
            break
        except Exception as e:
            print("Retrying connection in 5 seconds.")
            time.sleep(5)
    #pprint.pprint(info)
    #print(f"the transfers length is {len(info['transfers'])}")
    #pprint.pprint(info)
    if len(info['transfers']) == 1:
        theData = info["transfer"]
        someInfo = theData["address"]
        #print(someInfo)        
        height = info["transfer"]["height"]
        #quick zero conf
        #print(f"conf = {conf}")
        if conf == 0:
            if info["transfer"]["height"] == 0:
                return info["transfer"]
        else:
            if info["transfer"]["height"] != 0:
                return info["transfer"]
    else:
        for x in info["transfers"]:
                main(x,1,1)

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


if __name__ == '__main__':
    tx_id = sys.argv[1]
    
    #feed a specific txid 
    #tx_id = "98d754375dffe284504c820bca35f24d0261e50989c4f30561657e5c87982a1f"
    '''
    with open('txids', "r") as f:
        #f.write(tx_id)
        #f.write("\n")
        mylist = f.read().splitlines()
        for line in mylist:
            main(line,1)
            print(line)
            time.sleep(1)
    '''
    main(tx_id,0,0)

