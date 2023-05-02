let products = JSON.parse(sessionStorage.getItem('product'))
let table = document.querySelector('.estimate')
var total = products.map(obj => obj.pr).reduce((a,b) => a+b)
// .reduce((a,b) => a+b)

for(let i = 0; i < products.length; i++){
    let text = `
    <tr>
        <th>${products[i].category} ${products[i].details}</th>
        <th>${products[i].pr} рублей</th>
    </tr>
    `
    table.innerHTML += text
}

let text = `
<tr>
    <th colspan="2" style="text-align: right; right: 5%; position: relative;">Итоговая цена: ${total} рублей</th>
</tr>
`
table.innerHTML += text

let btnP = document.querySelector('.btnPay')

btnP.addEventListener('click', function(){
    let info = JSON.parse(sessionStorage.getItem('info'))

    async function saveOrder(){
        let sendInfo = {
            "info": info,
            "products": products
        }
        let response = await fetch('/addEstimate', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(sendInfo)
        });
        let result = await response.json()

        if (result.response == true){
            alert ('Заказ оформлен!')
            window.location.href = '/pages/managerStorage'
        } else alert('Ошибка отправки данных6 попробуйте позднее!')
    }

    saveOrder()

    console.log(info)
    console.log(products)
})