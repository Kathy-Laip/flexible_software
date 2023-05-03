var request = new XMLHttpRequest()

request.open('POST', '/getProductsOnManager', true)

const p = new Promise((res, rej) => {
    request.onload = () => {
        var dataAboutProduct = request.responseText
        res(dataAboutProduct)
    }
}).then(dataAboutProduct => {
    getProducts(dataAboutProduct)
})

async function getProducts(dataAboutProduct){
    var infoProducts = JSON.parse(dataAboutProduct)
    console.log(infoProducts)

    insertINtoProducts(infoProducts.products)

    function insertINtoProducts(infoProducts){
        var container = document.getElementById('products')
        for(let i = 0; i < infoProducts.length; i++){
            var textProduct = `<div class="containerProduct">
            <button class='deleteLesson'>&times;</button>
            <div class="textProduct">
                ${infoProducts[i].type} <br> ${infoProducts[i].description} <br> ${infoProducts[i].cost} рублей
            </div>
        </div>  <div class="containerForProduct" style="background-color: rgba(0,0,0,0.0); height: 30px; bottom: 0; width: 1px;"></div>`
            container.innerHTML += textProduct
        }
    }


    var deleteLesson = document.getElementsByClassName("deleteLesson");
    for(let i = 0; i < deleteLesson.length; i++){
        deleteLesson[i].addEventListener('click',  function(e) {
            var parent = e.target.closest(".containerProduct")
            var text = parent.querySelector('.textProduct').innerHTML.split('<br>').slice(0,2).map(el => el.trim())
            async function deleteProduct(){
                let response = await fetch('/deleteProduct', {
                    method: 'POST',
                    body: JSON.stringify(text),
                    headers: {
                        'Accept' : 'application/json',
                        'Content-Type' : 'appliction/json'
                    }
                }) 
                let result = await response.json()

                if(result.res == true){
                    parent.closest('.containerProduct').remove();
                } else alert('Что-то пошло нет так...')
            }
            deleteProduct()
        }, false)
    }
}

request.send()