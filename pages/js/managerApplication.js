var request = new XMLHttpRequest()

request.open('POST', '/getStuffOnManager', true)

const p = new Promise((res, rej) => {
    request.onload = () => {
        var dataAboutProduct = request.responseText
        res(dataAboutProduct)
    }
}).then(dataAboutProduct => {
    getStuff(dataAboutProduct)
})

async function getStuff(dataStuff){
    var infoStuff = JSON.parse(dataStuff)
    console.log(infoStuff)

    // console.log(sessionStorage.getItem('managerID'))

    insertIntoStuffInCategory(infoStuff.category)

    function insertIntoStuffInCategory(infoStuff){
        var container = document.getElementById('category')
        for(let i = 0; i < infoStuff.length; i++){
            var textProduct = `<option value="${infoStuff[i].type}">${infoStuff[i].type}</option>`
            container.innerHTML += textProduct
        }
    }

    document.getElementById('category').addEventListener('change', function(){
        let productChange = document.getElementById('product')
        productChange.innerHTML = '<option value=""></option>'
        let type = this.value

        var productType = infoStuff.stuff.filter(obj => obj.type === type)
        for(let pos of productType){
            if(pos.description === null){
                continue
            } else {
                productChange.innerHTML += `<option value="${pos.description}">${pos.description}</option>`
            }
        }
    })

    let product = []

    document.querySelector('.addProduct').addEventListener('click', function(){
        var nameProduct = document.getElementById('product').value
        var categoryProduct = document.getElementById('category').value
        var countProduct = document.getElementById('count').value
        var btnOF = document.querySelector('.arrange')
        var price

        var listProduct = document.querySelector('.listOfProducts')
        if (nameProduct == ''){
            for (let product of infoStuff.stuff){
                if(product.type == categoryProduct){
                    price = product.cost
                }
            }

            let item = {
                category: categoryProduct,
                pr: price,
                details: '',
                count: 1
            }

            listProduct.innerHTML += `<div class="containerForProduct">
            
        <div class="textForProduct">
            ${categoryProduct} <br>  Цена: ${price} рублей 
        </div>
    </div>`
            product.push(item)
        } else {
            for (let product of infoStuff.stuff){
                if(product.type == categoryProduct && product.description == nameProduct){
                    price = product.cost * Number(countProduct)
                }
            }

            let item = {
                category: categoryProduct,
                pr: price,
                details: nameProduct,
                count: Number(countProduct)
            }
    
            listProduct.innerHTML += `<div class="containerForProduct">
            <div class="textForProduct">
                ${categoryProduct} <br> ${nameProduct} <br> Цена: ${price} рублей <br> Количество: ${countProduct}
            </div>
        </div>
            `
            product.push(item)
        }
        
    }) 

    document.querySelector('.arrange').addEventListener('click', (listProduct) => {
        let nameDeceased = document.getElementById('nameDeceased').value
        let dateOfDeath = document.getElementById('dateOfDeath').value
        let dataPassport = document.getElementById('dataPassport').value
        let clientName = document.getElementById('clientName').value
        let dataPassportClient = document.getElementById('dataPassportClient').value
        let address = document.getElementById('address').value


        let masInfo = [ nameDeceased, dateOfDeath, dataPassport, clientName, dataPassportClient, address]
        if(masInfo.every(element => element !== '')){
            let manID = sessionStorage.getItem('managerID')
            let masInfo = {"nameDeceased": nameDeceased, "dateOfDeath": dateOfDeath, "dataPassport": dataPassport, "clientName": clientName, "phoneNumberClient": dataPassportClient, "address": address, "manageriD": manID}
            sessionStorage.setItem('product', JSON.stringify(product))
            sessionStorage.setItem('info',JSON.stringify(masInfo))
            window.location.href = '/pages/managerEstimate.html'
        } else alert('Заполните все поля!')
    })
}

//<div class="containerForProduct" style="background-color: rgba(0,0,0,0.0); height: 30px; bottom: 0;"></div>

request.send()