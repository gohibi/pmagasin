console.log('youpppppppppppppiiiiiiiiii');
var formid = document.getElementById('formComment')
if(formid){
    formid.addEventListener("submit",submitHandler);
}
function submitHandler(e){
    e.preventDefault();
    $.ajax({
        method: $(this).attr('method'),
        url: $(this).attr('action'),
        data: $(this).serialize(),
        dataType: "json",
        success: function (response) {
            console.log("bara va payer")

            if (response.bool == true){
                var htmlString = "Commentaire ajouté avec succès!"
               $('#review-success').html(htmlString);
               $('#formComment').hide();
               
            }
        }
    });
}


$(document).ready(function () {
    $('.filter-checkbox').on('click', function () {
        let filter_object = {};



        // let min_price = $('#max_price').attr('min')
        // let max_price =  $('#max_price').val()

        // filter_object.min_price = min_price
        // filter_object.max_price = max_price

        $('.filter-checkbox').each(function () {
            let filter_value = $(this).val();
            let filter_key = $(this).data('filter');

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function (x) {
                return x.value;
            });
        });

        filter_object['page'] = 1; // Default to first page

        $.ajax({
            url: '/filter-products/',
            data: filter_object,
            dataType: 'json',
            beforeSend: function () {
                console.log('Sending data...');
            },
            success: function (response) {
                console.log(response);
                $('.footer-hide').hide();
                $('#filtered-product').html(response.data);
            }
        });
    });

    // Pagination click event
    $(document).on('click', '.pagination a', function (event) {
        event.preventDefault();
        let page_number = $(this).attr('href').split('page=')[1];

        let filter_object = {};
        $('.filter-checkbox').each(function () {
            let filter_value = $(this).val();
            let filter_key = $(this).data('filter');

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function (x) {
                return x.value;
            });
        });

        filter_object['page'] = page_number;

        $.ajax({
            url: '/filter-products/',
            data: filter_object,
            dataType: 'json',
            beforeSend: function () {
                console.log('Sending data...');
                
            },
            success: function (response) {
                console.log(response);
                
                $('#filtered-product').html(response.data);
             
            }
        });
    });


});

$('.add-to-cart-btn').on("click" , function(){

        let val_this = $(this);
        let index = val_this.attr("data-index")
    
        let quantity = $(".product-quantity-" + index).val();
        let product_id = $('.product-id-' + index).val();
    
        let product_title = $('.product-title-' + index).val();
        let product_price = $(".current-product-price-" + index).text();
    
        let product_pid = $(".product-pid-" + index).val();
        let product_image = $(".product-image-" + index).val()
       
    
    
        console.log('quantity:', quantity);
        console.log('id:', product_id);
        console.log('pid:', product_pid);
        console.log('image:', product_image);
        console.log('produit-title:', product_title);
        console.log('index:', index);
        console.log('prix:', product_price);
        console.log('element actuel:',val_this);
    
        $.ajax({
            url:'/ajouter-au-panier/',
            data:{
                'id':product_id,
                'pid':product_pid,
                'image':product_image,
                'quantity':quantity,
                'title':product_title,
                'price':product_price
            },
            dataType:'json',
            beforeSend:function(){
                console.log('Ajouter un produit au panier!')
            },
            success:function(response){
                val_this.html('✔')
                console.log('Produit ajouté au panier!')
                $('#cart-items-count').text(response.totalitems)
                $('.details').hide()
            }
    
        })
        
    })

$('.remove-product').on('click',function(){
    let product_id = $(this).attr('data-product')
    let this_val = $(this)

    console.log('ID:',product_id)
    
    $.ajax({
        url:'/supprimer-produit-du-panier/',
        data:{
            'id':product_id
        },
        dataType:'json',
        beforeSend:function () {
            this_val.hide();
          },
        success:function(response){
            this_val.show();
            $('#cart-items-count').text(response.totalitems);
            $('#cart-list').html(response.data);

        }
    })
 });

 $('.edit-product').on('click',function(){
    let product_id = $(this).attr('data-product')
    let this_val = $(this)
    let product_quantity = $('.product-quantity-'+ product_id).val()

    console.log('ID:',product_id)
    console.log('quantity',product_quantity)
    
    $.ajax({
        url:'/modifier-produit-du-panier/',
        data:{
            'id':product_id,
            'quantity':product_quantity
        },
        dataType:'json',
        beforeSend:function () {
            this_val.hide();
          },
        success:function(response){
            this_val.show();
            $('#cart-items-count').text(response.totalitems);
            $('#cart-list').html(response.data);

        }
    })
 });

 $(document).on("click",'.add-to-wishlist',function(){
    let product_id = $(this).attr('data-product-item');
    let val_this = $(this)
    console.log('ID:',product_id)
    $.ajax({
        url:"/ajouter-wishlist/",
        data:{
            'id':product_id, 
        },
        dataType:'json',
        beforeSend:function () {
            val_this.html('✔')
          },
        success:function(response){
            if (response === true){
                console.log('Ajouter a la wishlist...')
            }
           
           

        }
    })

 });


 $(document).on("click",'.remove-to-wishlist',function(){
    let product_id = $(this).attr('data-wishlist-product');
    let val_this = $(this)
    console.log('ID:',product_id)

    $.ajax({
        url:'/supprimer-wishlist/',
        data:{
            'id':product_id,
        },
        dataType:'json',
        beforeSend:function(){
            console.log("Deleting product from wishlist..")
        },
        success:function(response){
            $('#wishlist-list').html(response.data)
            $('.tbody-text').text('Empty wishlist')
        }
    })

 });

// $('#add-to-cart-btn').on("click" , function(){

//     let val_this = $(this);
  

//     let quantity = $("#product-quantity").val();
//     let product_id = $('.product-id').val();
//     let product_title = $('.product-title').val();
//     let product_price = $("#current-product-price").text();



//     console.log('quantité :', quantity);
//     console.log('produit-id :', product_id);
//     console.log('produit-title :', product_title);
//     console.log('prix:', product_price);
//     console.log('element actuel:',val_this);

//     $.ajax({
//         url:'/ajouter-au-panier/',
//         data:{
//             'id':product_id,
//             'quantity':quantity,
//             'title':product_title,
//             'price':product_price
//         },
//         dataType:'json',
//         beforeSend:function(){
//             console.log('Ajouter un produit au panier!')
//         },
//         success:function(response){
//             val_this.html('Article ajouté au panier')
//             console.log('Produit ajouté au panier!')
//             $('#cart-items-count').text(response.totalitems)
//         }

//     })
    
// })
 
 