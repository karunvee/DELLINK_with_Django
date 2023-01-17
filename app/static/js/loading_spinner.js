const spinnerBox = document.getElementById('spinner-box')
const dataBox = document.getElementById('data-box')

        $.ajax({
            type: 'GET',
            url: '/',
            success:function(response){
                setTimeout(()=>{
                    spinnerBox.classList.add('invisable')
                    // console.log(response)
                },1500)
            },
            error: function(error){
                setTimeout(()=>{
                    spinnerBox.classList.add('invisable')
                    dataBox.innerHTML = '<b>Failed to load this page!</b>'
                },1500)
            }
        })