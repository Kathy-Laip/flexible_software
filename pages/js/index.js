const requset = new XMLHttpRequest()
var btn = document.querySelector('.buttonLogIn')

class User {
    constructor(options){
        this.login = options.login,
        this.password = options.password
    }

    async authorization(){
        let response = await fetch('/signin', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(user)
        });
        let result = await response.json()
        console.log(result)
    }
}

var user
const btnClick = () => {
    const log = document.querySelector('#email').value
    const pas = document.querySelector('#password').value
    user = new User({login: log, password: pas})
    user.authorization()
}
