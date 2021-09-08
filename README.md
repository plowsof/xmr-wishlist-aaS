# Live XMR wishlist as a service

It will serve / push updated to a Json array file on github for any external websites to fetch and display.
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

Example of progressbar/num contributors here https://plowsof.github.io/    

Ideally you would begin with a fresh wallet with no activity.    
However, if you're setting this up after the fact then you will need to export the view wallet history
then see ```helpers/make_txids.py```. Slight modification to ```wishlist-aas.py```'s __main__ function to feed the tx's 1 by 1.

# Support
I enjoyed making this (because of how out of my depth i am with front end stuff), i will support you if you reach out to me with issues/q's reg. this.
And if you want to show support to me, my xmr address is below, much appreciated! :')
```
86aSNJwDYC2AshDDvbGgtQ17RWspmKNwNXAqdFiFF2Db91v9PC26uDxffD9ZYfcMjvJpuKJepsQtELAdmXVk85E1DsuL6rG
```
