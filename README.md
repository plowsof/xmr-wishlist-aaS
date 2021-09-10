# Live XMR wishlist as a service

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
```

In your .js file:
```
see helpers/app.js
```

Example of progressbar/num contributors here https://moneroart.neocities.org/

## Setting up with an unused wallet
- Modify ```helpers/make_wishlist.py``` to create your json wishlist, containing the subaddresses/descriptions of each wish.
- Upload this file to your github and set the correct URL / github token values.
- Configure your monero-wallet-rpc's 'tx-notify' value to call ```wishlist-aas.py``` with python3
- Make sure that the pyhton script is using the correct ip:port for your rpc-wallet

## Setting up with an 'already used wallet'
Ideally you would begin with a fresh wallet with no activity. However:  
- Open a synched view wallet up displaying the correct balance and export the view wallet history (.csv file)
- Then see ```helpers/make_txids.py```. Slight modification to ```wishlist-aas.py```'s __main__ function to feed the tx's 1 by 1.
- Assuming you have used ```helpers/make_wishlist.py``` and uploaded the json and have your URLs/Tokens set, revert the changes to main().

# Support
I enjoyed making this (because of how out of my depth i am with front end stuff), i will support you if you reach out to me with issues/q's reg. this.
And if you want to show support to me, my xmr address is below, much appreciated! :')
```
86aSNJwDYC2AshDDvbGgtQ17RWspmKNwNXAqdFiFF2Db91v9PC26uDxffD9ZYfcMjvJpuKJepsQtELAdmXVk85E1DsuL6rG
```
