from django.contrib import admin
from core.models import Product,ProductImage,Vendor,ProductReview,Category,CartOrder,CartOrderItems,Address,Wishlist


class ProductImageAdmin(admin.TabularInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
    list_display =['user','category','title','product_image','slug','description','price','product_status','featured','date']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk','cid','title','category_image']

class VendorAdmin(admin.ModelAdmin):
    list_display = ['pk','title','vendor_image']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product','user','rating','review','date']

class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['status_payment','product_status']
    list_display = ['user','price','date_order','status_payment','product_status']

class CartOrderitemAdmin(admin.ModelAdmin):
    list_display = ['order','invoce_no','item','image','quantity','price','total']


class AddressAdmin(admin.ModelAdmin):
    list_display =['user','address','status']



class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user','product','date']



admin.site.register(Product,ProductAdmin)
admin.site.register(Vendor,VendorAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(ProductReview,ProductReviewAdmin)
admin.site.register(CartOrder,CartOrderAdmin)
admin.site.register(CartOrderItems,CartOrderitemAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Wishlist,WishlistAdmin)