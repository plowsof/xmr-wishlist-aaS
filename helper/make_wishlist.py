
import pprint
import json
from datetime import datetime

def wishlist_add_new(goal,address,desc):
    global wishlist
    app_this = { 
        "goal":goal,
        "total":0,
        "contributors":0,
        "address":address,
        "desc": desc,
        "percent": 0
    } 
    wishlist.append(app_this)

wishlist = []

wishlist_add_new(0.5,"8BQE9MKuMt23pfhG4zoH4x8prqb8w1nKVXoDE7yAGXTGFmtawVPA1aaAFvjj7XFjASZtMXuyfhY9uVBP8xxtBVRnRcLgTXe","Dressed as a miner / mining")
wishlist_add_new(0.4,"84KDo28eAXk6hvRc1cZVmMGwpFT7bCEGG4VEXP2tigg6Ab7zYMBf45vGHg9hjUWqEUCimLrNhVMca1WFKTPnB4XRE35nn6L","Walking doggirl Wownero-chan on a leash")
wishlist_add_new(0.4,"89gWT9S5mgx3gCJeADaS3Y57iBBot2QDVWaQweHbRxqphuHHfBJySiASCM8QRMRUhC6B2Mud2crtXHKCRkx96A8SJQAsUCk","Headpatting doggirl Wownero")
wishlist_add_new(0.3,"85hAguPjyR9Rxh7gBbs37H6vWTwBpEb7Q3h3uScERzZD6PParihxrJbGdzaD7UhvskhYTnr34auVpdCLR9RYD5rQJA8bLxu","Posed with an assault rifle")
wishlist_add_new(0.5,"8ADf1FkqBe5Ky7yu7aMsT3UKHBAmEou6AQk2TWZLdErRLsd7FbRUp5wiK1DWKAZpajjZkB78uRq8FNspq9kHKTBJ6jfZkQL","Sitting at a computer assembling an FGC-9 w/ 3D printer in background")
wishlist_add_new(0.3,"83AHkBEtqoKEcXbWRLQNhVgpTifv59WQsjfsev99Jwp96unxEH5pXfyby7DDfEndHq4UvtUzJHZFd4sJKtUKAJPuBVZuCWn","Polkadot sweater")
wishlist_add_new(0.5,"84rYVxTTyWkYUtu71HDqejJD2g4APut2wRr4RGbd4Ade3NYTfdkLoPo6erP1aM9ax5SHthCv1dCL8a5CHjYSp8jb6WBb4ZR","Sitting on a throne")
wishlist_add_new(0.4,"86Z68Znx9FGgjvXqcDJfeuQ6S21h2EHqP617txPgXedkES6PDEaU8SyF4uUrGPW1X4h6p9hQ8U2XZWKUVLBFNpS5URedzme","Spanking IRS-chan over her knee")
wishlist_add_new(0.5,"84ASBdQraPtceff6qiazhfZ4yB8bZdmaRbDnGXfJBHRhXJXu1oqzLvgH4cVhF8higtN1BysTJdU9fCw9CkKuVjgL9d9azAq","Blowing a dandelion")

thetime = datetime.now()
total = {
	"total": 0,
	"contributors": 0,
	"modified": str(thetime)
}




print(json.dumps([wishlist,total], indent=4, sort_keys=True))
