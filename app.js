let modified = "0"

async function getWishlist() {
    let ran_int = Math.floor(Math.random() * 100000)
    let url = 'https://raw.githubusercontent.com/plowsof/plowsof.github.io/main/wishlist/wishlist-data.json?uid=' + ran_int;
    try {
        let res = await fetch(url);
        return await res.json();
    } catch (error) {
        alert(error);
    }
}

async function renderWishlist() {
    let wishlist = await getWishlist();
    modified_live = wishlist[1]["modified"]
    if (modified != modified_live){
        modified = modified_live
        let html = '';
        let id = 0
        let ran_int = Math.floor(Math.random() * 101);
        wishlist[0].forEach(wish => {
        let total = wish.total.toFixed(2)
        let htmlSegment =`  <div class ="wish">
                                <li>
                                    ${wish.desc} : <i class="fundgoal">Raised ${total} of ${wish.goal} XMR   <progress id="file" max="100" value="${wish.percent}">${wish.percent}%</progress> Contributors: ${wish.contributors}</i>
                                    <label for="file"></label>
                                    <p class="subaddresses" id="${id}" onclick=CopyToClipboard('${id}')>${wish.address}</p><br/>
                                </li>
                            </div>`;
            html += htmlSegment;
        id += 1;
        });

        let container = document.querySelector('.container');
        container.innerHTML = html;
        let total_main = document.querySelector('.total_main');
        total_main.innerHTML = wishlist[1]["total"];
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
    navigator.clipboard.writeText(textContent)
    .then(() => { alert(`Address Copied!`) })
    .catch((error) => { alert(`Copy failed! ${error}`) })
}
//on page load - render the wishlist. set a 'time updated variable from the json' then loop compare
//infinite loop

renderWishlist()
setInterval('renderWishlist()',5000)
