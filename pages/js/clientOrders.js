const requset = new XMLHttpRequest()
const clientID = sessionStorage.getItem('clientID')

let response = await fetch('/signin', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(clientID)
});
let result = await response.json()


if (){
    
} 


