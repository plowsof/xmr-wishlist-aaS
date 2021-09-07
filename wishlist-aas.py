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

#os.chdir("/your/scripts/dir")
wishlist = []
repo_name =  "plowsof.github.io"
repo_dir = "wishlist"
git_token = "ghp_hunter2***************"
json_url = "https://raw.githubusercontent.com/plowsof/plowsof.github.io/main/wishlist/wishlist-data.json"

def getJson():
    #must get the latest json as it may have been changed
    x = requests.get(json_url)
    return json.loads(x.text)

def main(tx_id):
    #check height
    saved_wishlist = getJson()
    tx_data = checkHeight(tx_id)
    if tx_data:
        tx_data["amount"] = formatAmount(tx_data["amount"])
        found = 0
        main_fund = saved_wishlist[1]["total"]
        for i in range(len(saved_wishlist[0])):
            try:
                #print(saved_wishlist[i])
                if saved_wishlist[0][i]["address"] == tx_data["address"]:
                    found = 1
                    #contributor += 1 
                    saved_wishlist[0][i]["contributors"] += 1
                    #total += amount
                    saved_wishlist[0][i]["total"] += float(tx_data["amount"])
                    
                    print(f"after:{saved_wishlist[0][i]}")
                    #if total => goal its 100%
                    if float(saved_wishlist[0][i]["total"]) >= float(saved_wishlist[0][i]["goal"]):
                        #fully funded [ do something special e.g. make a tweet ...]
                        saved_wishlist[0][i]["percent"] = 100
                        extra_xmr = float(saved_wishlist[0][i]["total"]) - (saved_wishlist[0][i]["goal"])
                        if extra_xmr > 0:
                            saved_wishlist[0][i]["total"] = saved_wishlist[0][i]["goal"]
                            print(saved_wishlist[0][i]["total"])
                            #add to the 'main fund'
                            saved_wishlist[1]["total"] += float(extra_xmr)
                    else:
                        saved_wishlist[0][i]["percent"] = float(saved_wishlist[0][i]["total"]) / float(saved_wishlist[0][i]["goal"]) * 100         
                    break
            except Exception as e:
                raise e
        if found == 0:
            extra_xmr = tx_data["amount"]
            #donation received on an address not on the wishlist
            saved_wishlist[1]["total"] += float(extra_xmr)
            saved_wishlist[1]["contributors"] += 1

        #finished. unless "batched" doesn't exist
        saved_wishlist[0] = sorted(saved_wishlist[0], key=lambda k: k['percent'],reverse=True)
        modified = str(datetime.now())
        saved_wishlist[1]["modified"] = modified
        print(modified)
        pickle.dump(saved_wishlist, open( "wishlist.p", "wb+" ) )
        if not os.path.isfile("batched"):
            #create "batched"
            with open("batched", "w+") as f:
                f.write("1")
            time.sleep(30)
            createHtml()
            #push file with git
            #delete batched
            os.remove("batched")


def createHtml():
    saved_wishlist = pickle.load(open("wishlist.p", "rb"))
    #create json
    with open("wishlist-data.json", "w") as f:
        json.dump(saved_wishlist, f, indent = 6)
    uploadtogit("wishlist-data.json","wishlist-data.json")

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
    theData = info["transfer"]
    someInfo = theData["address"]
    #print(someInfo)        
    height = info["transfer"]["height"]
    #quick zero conf
    if conf == 0:
        if info["transfer"]["height"] == 0:
            return info["transfer"]
    else:
        if info["transfer"]["height"] != 0:
            return info["transfer"]

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
    print(outfile)
    # Upload to github
    git_file = repo_dir + "/" + outfile
    contents = repo.get_contents(git_file)
    repo.update_file(contents.path, "committing files", content, contents.sha, branch="main")
    print(git_file + ' UPDATED')


if __name__ == '__main__':
    #mitigate flooding donations
    time.sleep(random.randint(1, 20))
    tx_id = sys.argv[1]
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
    main(tx_id)
