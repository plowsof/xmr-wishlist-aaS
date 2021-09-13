let modified = "0"

async function getWishlist() {
    let ran_int = Math.floor(Math.random() * 100000)
    //let url = 'https://raw.githubusercontent.com/plowsof/plowsof.github.io/main/wishlist/wishlist-data.json?uid=' + ran_int;
    let url = "https://raw.githubusercontent.com/plowsof/funding-xmr-radio/main/json/wishlist-data.json?uid=" + ran_int;
    try {
        let res = await fetch(url);
        return await res.json();
    } catch (error) {
        return null;
    }
}

async function renderWishlist() {
    let wishlist = await getWishlist();
    modified_live = wishlist["metadata"]["modified"]
    if (modified != modified_live){
        modified = modified_live
        let html_equip = '';
        let html_subsc = '';
        let id = 0
        let ran_int = Math.floor(Math.random() * 101);
        wishlist["wishlist"].forEach(wish => {
        let qrcheck = document.getElementById(`qr-${wish.address}`);
        let qrchecked = (qrcheck && qrcheck.checked)?" checked":"";
        //alert(qrchecked)
        wish.percent = wish.total / wish.goal * 100;
        let total = wish.total.toFixed(2)
        let goal = wish.goal.toFixed(2)
        //alert(wish.address)
        let ahead1 = wish.address.substr(0,4)
        let ahead2 = wish.address.substr(4,4)
        let atail1 = wish.address.substr(-8,4)
        let atail2 = wish.address.substr(-4,4)
        let atail = wish.address.substr(-5,5)
        let something = ""
        let address = something.concat(ahead1, " ", ahead2," .. ", atail1, " ", atail2)
        wish.percent = 50
        var current_percent = wish.percent;
        let ascii_progress = ''
        for (n = 0; n < 20; n++) {
            if (current_percent < (n+1)*5) {
                ascii_progress = ascii_progress.concat("░"); // alt-176 
            }
            else {
                ascii_progress = ascii_progress.concat("▓"); // alt-178
                 }    
        }
        //alert(ascii_progress)
        //let address = wish.address
        //<progress id="file" max="100" value="${wish.percent}">${wish.percent}%</progress>
                    let qr =`
                                <input id="qr-${wish.address}" type="checkbox" name="tabs" class="accordion"${qrchecked}>
                                <label for="qr-${wish.address}" class="accordion button">QRcode</label>
                                <br><div class="qr-content">
                                    <p><a class="qr" href="monero:${wish.address}?tx_description=${encodeURIComponent(wish.title)}"><img src="${wish.qr_img_url}"></a></p>
                                </div>`
        let htmlSegment =`               <div class ="wish">
                                    <li id=${wish.id}>
                                        <p class="wishtitle">${wish.description}</p> 
                                        <i class="fundgoal">Raised ${total} of ${goal} XMR [<span id="ascii-progress-bar">${ascii_progress}</span>] Inputs: ${wish.contributors}</i>
                                        <p class="subaddress" id="${wish.address}" onclick=CopyToClipboard('${wish.address}')  >${address}</p> ${qr} 
                                    </li> </div>`;


            //if type == equip then add to...
            if (wish.type == "equip"){
                html_equip += htmlSegment
            }
            else{
                html_subsc += htmlSegment
            }
        id += 1;
        });
        //if type == something then add to that
        let container = document.querySelector('.equipment');
        container.innerHTML = html_equip;
        let container2 = document.querySelector('.recurring');
        container2.innerHTML = html_subsc;
        //let total_main = document.querySelector('.total_main');
        //total_main.innerHTML = wishlist["metadata"]["total"];
    }

}

function CopyToClipboard(id)
{
    var node = document.getElementById(id);
    htmlContent = node.innerHTML;
    // htmlContent = "Some <span class="foo">sample</span> text."
    textContent = node.textContent;
    // textContent = "Some sample text."
    node.focus();
    navigator.clipboard.writeText(id)
    .then(() => { alert(`Address Copied!`) })
    .catch((error) => { alert(`Copy failed! ${error}`) })
}


//on page load - render the wishlist. set a 'time updated variable from the json' then loop compare
//infinite loop

renderWishlist()
setInterval('renderWishlist()',2000)


