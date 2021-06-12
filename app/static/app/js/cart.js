var updateBtns = document.getElementsByClassName('update-cart')

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click',function(){
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log('productId:',productId,'action:',action)
        
        updateUserOrder(productId,action)
    })    
}

function updateUserOrder(productId,action){
    let url = '/updateItem/'
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({
            'productId':productId,
            'action':action
        })
    })
    .then((response) => {
        if (!response.ok) {
            // error processing
            throw 'Error';
        }
        return response.json()
    })

    .then((data)=>{
        console.log('data:',data)
        location.reload();
    })
}