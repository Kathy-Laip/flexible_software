const requset = new XMLHttpRequest()
const managerID = sessionStorage.getItem('managerID')
console.log(managerID)
const boxOrders = document.getElementById('products')

class Order {
    constructor(options){
        this.id = options.id
        this.price = options.prices
        this.status = options.status
        this.address = options.address
        this.deadmans_name = options.deadmans_name
    }
}

const orders = []

async function sendManagerID(){
    let infoOrders = {
        id: managerID,
        all: true
    }
    let response = await fetch('/getOrdersByManager', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(infoOrders)
    });
    let result = await response.json()
    console.log(typeof(result))

    if (result.orders !== []){
        for (let order of result.orders){
            orders.push(new Order(order))
            let boxOrdersText = `<div class="containerOrder">
                <div class="textOrder">
                    <strong>Заказ №${order.id} </strong> <br> Цена: ${order.price} рублей <br> Адресс: ${order.address} <br> ФИО покойного: ${order.deadmans_name} <br> статус: ${order.status}
                </div>
            </div> `
            boxOrders.innerHTML +=  boxOrdersText
        }
    }
}

sendManagerID()

// requset.send()