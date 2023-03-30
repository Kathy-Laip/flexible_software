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
            <div class="textProduct">
                ${infoProducts[i].type} <br> ${infoProducts[i].description} <br> ${infoProducts[i].cost} рублей
            </div>
        </div>`
            container.innerHTML += textProduct
        }
    }
}

request.send()