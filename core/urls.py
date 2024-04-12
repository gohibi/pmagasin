from django.urls import path,include
# from . import views
from core.views import (index,list_product_category,product_detail,tag_list,
list_product,ajax_add_review,filter_product,add_to_cart,cart,
delete_item_cart,update_item_cart,checkout,payment_success,payment_failed,
customer_dashboard,order_detail,get_wishlist,wishlist,remove_wishlist)


# from .views import ListProductView
app_name = "core"

urlpatterns = [
    path('',index,name="index"),
    path('categorie-produit/<cid>',list_product_category,name="category-product"),
    path('nos-produits',list_product,name="products"),
    path('detail-produit/<pid>/<str:slug>',product_detail,name="detail-product"),
    path('produits/tag/<str:slug_tag>',tag_list,name="tags"),
    path('detail-produit/ajouter-commentaire/<pid>/<str:slug>',ajax_add_review,name="add-review"), 
    path('filter-products/',filter_product,name="filter-product"),
    path('ajouter-au-panier/', add_to_cart , name="add-to-cart"),
    path('mon-panier/',cart,name="cart"),
    path('supprimer-produit-du-panier/', delete_item_cart,name="delete-cart"),
    path('modifier-produit-du-panier/', update_item_cart,name="update-cart"),
    path('checkout-cart/',checkout,name="checkout"),
    path('payment-completed/',payment_success,name="payment-success"),
    path('payment-failed/',payment_failed,name="payment-failed"),
    path('paypal/',include('paypal.standard.ipn.urls')), 
    path('tableau-de-bord/',customer_dashboard,name="dashboard"),
    path('tableau-de-bord/detail-order/<int:id>',order_detail,name="order-detail"),
    path('wishlist/',wishlist,name="wishlist"),
    path('ajouter-wishlist/',get_wishlist,name='add-wishlist'),
    path('supprimer-wishlist/',remove_wishlist,name='remove-wishlist'),



    # path('nos_produits',views.ListProductView.as_view , name="products")
]