##XMR wishlist as a service

This is for people who would like to host a wishlist on their (free) githubpages site.    


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

Ideally you would begin with a fresh wallet with no activity.    
However, if you're setting this up after the fact then you will need to export the view wallet history
then see ```helpers/make_txids.py```. Slight modification to ```wishlist-aas.py```'s __main__ function to feed the tx's 1 by 1.
