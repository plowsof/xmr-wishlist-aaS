# Live XMR wishlist as a service

## FlipStarter
In an experiment to explore other funding alternatives to the CCS, (and extend the outreach of Monero), i have opened up a Flipstarter to make this multi-currency. XMR/BCH/BTC. And in doing so, gain funding to improve this as a whole to make it more userfiendly / add new features, which is being developed [here](https://github.com/plowsof/flipstarter-waas-wip). I have been somewhat successful with my goals, as my new list is being used by someone else who has had one of their wishes successfully funded @ [Ruckniums Donation page](https://rucknium.me/donate)

## About
It will serve / push updates to a Json array file on github for any external websites to fetch and display.
What you need:
```
A github account / access token for the script (modify the variables accordingly)
monero-wallet-rpc monitoring a view-only wallet
```
Example json data
```
https://github.com/plowsof/plowsof.github.io/blob/main/wishlist/wishlist-data.json
```
The json array is 'live' and changes will be pushed to your page (adding/removing)

In your monero-wallet-rpc config file:
```bash
tx-notify=/usr/bin/python3 /path/to/wishlist-aas.py %s
```

In your .html file:
```html
<div class="container"></div>
<script src="js/app.js"></script>
<link href="main.css" rel="stylesheet" type="text/css" media="all">
```

In your .js file:
```
see helpers/app.js
```

## Examples 
https://xmr.radio/funding src @ https://github.com/plowsof/funding-xmr-radio (i had full creative control over the UI for this one, so im especially proud!)    
https://funding.monerujo.app/    
https://moneroart.neocities.org/    

## Setting up with an unused wallet
- Modify ```helpers/make_wishlist.py``` to create your json wishlist, containing the subaddresses/descriptions of each wish.
- Upload this file to your github and set the correct URL / github token values. (or ignore this step put it on your own server, im just poor ^^)
- Configure your monero-wallet-rpc's 'tx-notify' value to call ```wishlist-aas.py``` with python3
- Make sure that the pyhton script is using the correct ip:port for your rpc-wallet

## Setting up with an 'already used wallet'
Now using rpc call ```get_transfers``` to load the wallet history (if any found) (no more wasting time creating a csv file from the GUI).
- After creating a new wishlist, the wallet history will be imported into the json data (+= to contributors and amounts of the matching addresses)
- see ```load_old_txs``` in ```helpers/make_wishlist.py```

## Modifying your list
- An online json editor could be used to add/remove items easily. e.g:
- https://jsoneditoronline.org

## Updates
- QRimages generated for each subaddress + a custom logo see ```helpers/make_wishlist.py```
- USD amounts accepted for each wish - then converted to current XMR value + a % buffer (can be changed on the fly to readjust goals also)
- Generate a sub address for your wish if none is supplied see ```helpers/make_wishlist.py```. 
- Creating wishlist is now as simple as: (3rd arg is a wish 'type' to help display things on the front end)
```
create_new_wishlist(500,"Something special",None,"work")
create_new_wishlist(5,"buy me a coffee"86aSNJwDYC2AshDDvbGgtQ17RWspmKNwNXAqdFiFF2Db91v9PC26uDxffD9ZYfcMjvJpuKJepsQtELAdmXVk85E1DsuL6rG","gift")
```
# Support

This project has been fully funded by the Monero Outreach team @https://twitter.com/xmroutreach <3 

I enjoyed making this (because of how out of my depth i am with front end stuff), i will support you if you reach out to me with issues/q's reg. this.
And if you want to show support to me, my xmr address is below, much appreciated! :')
```
86aSNJwDYC2AshDDvbGgtQ17RWspmKNwNXAqdFiFF2Db91v9PC26uDxffD9ZYfcMjvJpuKJepsQtELAdmXVk85E1DsuL6rG
```
