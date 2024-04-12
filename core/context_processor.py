from core.models import Category , Address ,Product , Wishlist
from django.db.models import Count,Max,Min
from django.contrib import messages

def default(request):
    categories = Category.objects.all()
    min_max_price = Product.objects.aggregate(Min("price"),Max("price"))

    try:
        wishlist = Wishlist.objects.filter(user=request.user)
    except:
        messages.warning(request, "Connectez-vous avant d'avoir acces a votre wishlist")
        wishlist = 0
    try:
        addresses = Address.objects.get(user=request.user)
    except:
        addresses =None
    
    return {
        'categories':categories,
        'addresses':addresses,
        'min_max_price':min_max_price,
        'wishlist':wishlist,
    }