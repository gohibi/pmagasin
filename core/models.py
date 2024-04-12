from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from django.utils import timezone
from authusers.models import User
from taggit.managers import TaggableManager
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField



STATUS_CHOICES= (
      ('process', 'Processing'),
      ('shipped', 'Shipped'),
      ('delivered', 'Delivered'),
)

STATUS = (
      ('draft', 'Draft'),
      ('disabled', 'Disabled'),
      ('rejected', 'Rejected'),
      ('in_review', 'In Review'),
      ('published', 'Published'),
)

RATING= (
      (1,"★✰✰✰✰"),
      (2,"★★✰✰✰"),
      (3,"★★★✰✰"),
      (4,"★★★★✰"),
      (5,"★★★★★")
)

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id,filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True,length=10, max_length=15, prefix="CAT", alphabet="0123456789")
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category')

    class Meta:
        verbose_name_plural ="Categories"
        ordering = ['title']

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50">'%(self.image.url) )
    
    def __str__(self):
        return self.title
    

class Vendor(models.Model):
    vid = ShortUUIDField(unique=True,length=10, max_length=15 , prefix="VND", alphabet="0123456789")
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path)
    user = models.ForeignKey(User , on_delete=models.SET_NULL, null=True)
    # description = models.TextField(null=True,blank=True)
    description = RichTextUploadingField(null=True,blank=True)
    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    days_return = models.CharField(max_length=100)
    warrantly_period = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural ="Vendors"
        ordering =['title']

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" >' %(self.image.url))
    
    def __str__(self):
        return self.title
    
class Tags(models.Model):
    pass  

class Product(models.Model):
    pid = ShortUUIDField(unique=True,length=10, max_length=15 , prefix="PROD", alphabet="0123456789")
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path)
    # description = models.TextField(null=True,blank=True)
    description = RichTextUploadingField(null=True,blank=True)
    user = models.ForeignKey(User , on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True,related_name="categorie")
    price = models.DecimalField(max_digits=10,decimal_places=0)
    old_price = models.DecimalField(max_digits=10,decimal_places=0)
    # specifications= models.TextField(null=True,blank=True)
    specifications= RichTextUploadingField(null=True,blank=True)
    life = models.CharField(max_length=100)
    stock_count = models.CharField(max_length=100)

    tags =TaggableManager(blank=True)
    product_status = models.CharField(choices=STATUS,max_length=12)
    status =models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    sku  = ShortUUIDField(unique=True, length=4 , max_length=10 , prefix ="SKU",alphabet="0123456789")
    slug = models.SlugField(default="", null=False,max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    updated =models.DateTimeField(null=True,blank=True)
    
    class Meta:
        verbose_name_plural = "Products"
        ordering = ["-date"]
    
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" >'%(self.image.url))
   
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail-product' , kwargs={"slug":self.slug , "pid":self.pid})
    def get_precent(self):
        if self.old_price > 0:
            reduction = ( self.price / self.old_price)* 100
            return reduction
        return 0
    

class ProductImage(models.Model):
    images=models.ImageField(upload_to="products-images")
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,related_name="p_image")
    date=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Products Images"    


class CartOrder(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE)
      price = models.DecimalField(max_digits=10,decimal_places=0)
      date_order =models.DateTimeField(auto_now_add=True)
      status_payment=models.BooleanField(default=False)
      product_status=models.CharField(choices=STATUS_CHOICES,max_length=30,default="processing") 

      class Meta:
            verbose_name_plural = "Cart Orders"
            ordering = ["-date_order"]

      def __str__(self):
        return f'{self.user}-{self.price}'

class CartOrderItems(models.Model):
      order = models.ForeignKey(CartOrder,on_delete=models.CASCADE , related_name="order_item")
      invoce_no = models.CharField(max_length=200)
      product_status = models.CharField(max_length=200)
      item=models.CharField(max_length=200)
      image =models.CharField(max_length=200)
      quantity =models.IntegerField(default=0)
      price = models.DecimalField(max_digits=10,decimal_places=0)
      total= models.DecimalField(max_digits=10,decimal_places=0)

      class Meta:
            verbose_name_plural ="Cart Order Items"
            ordering = ["-order"]

      def order_image(self):
            return mark_safe('<img src="media/%s" width="50" height="50" />' % (self.image))
      def __str__(self):
        return f'{self.order}-{self.item}'

class ProductReview(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,related_name="review_dproduct")
    review =models.TextField()
    rating = models.IntegerField(choices=RATING,default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Products Reviews"
        ordering = ["-date"]
   
    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    

class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlists"
        ordering = ["-date"]
   
    def __str__(self):
        return self.product.title
    
class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    address = models.CharField(max_length=100,null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Addresses"
