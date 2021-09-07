#After exporting the view-wallet history in the monero gui, it can be parsed easily to get the txid's
#which will be fed to the 'wish list as a service' script

with open("monero-txs_1630975952.csv", "r") as f:
	lol = f.read().splitlines() 

for x in lol:
	with open('txids', 'a+') as f:
		f.write(x.split(',')[7])
		f.write("\n")