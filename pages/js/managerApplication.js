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

    console.log(sessionStorage.getItem('managerID'))

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
}

request.send()