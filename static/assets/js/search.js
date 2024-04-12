   $('#max_price').on("blur",function(){
        let min_price = $(this).attr('min')
        let max_price = $(this).attr('max')
        let current_price = $(this).val()

        console.log('min price:',min_price)
        console.log('max price:',max_price)
        console.log('current price:',current_price)

        if((current_price < parseInt(min_price)) || (current_price > parseInt(max_price) )){
            alert("Le prix des produits est compris entre "+min_price+ ' fcfa'+ ' et ' +max_price+' fcfa')
            $(this).val(min_price)
            $('#range').val(min_price)
            $(this).focus()

            return false
        }
    })

$('#form_search').submit(function(e){
    e.preventDefault()

    let formData ={
        recherche:$('#product').val(),
        min:$('#min').val(),
        max:$('#max').val(),
        
    };
    $.ajax({
        
    })


});

$(document).ready(function () {
    $('.filter-checkbox').on('click', function(){
        console.log('bara va payer');

        let filter_object = {}
        $('.filter-checkbox').each(function(){
            let filter_value = $(this).val();  
            let filter_key  = $(this).data('filter') //category

            console.log("valeur du filtre : ",filter_value); 
            console.log("clé du filtre : ",filter_key);

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter = '+ filter_key +']:checked')).map(function(x){
                return x.value ;

            });
        });

        filter_object['page'] = 1;

        console.log('filter object est' , filter_object);
        $.ajax({
            url:'/filter-products',
            data:filter_object,
            dataType:'json',
            beforeSend: function () {
                console.log('Sending data...')
                
              },
            success:function(response){
                console.log(response);
                console.log('filtrage reussi');
                $('#filtered-product').html(response.data)
            }
        });
    });
    


});