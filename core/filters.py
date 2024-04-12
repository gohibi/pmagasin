import django_filters
from core.models import Product


class ProductFilter(django_filters.FilterSet):
    # title = django_filters.CharFilter(field_name="Product",lookup_expr='icontains')
    # category__title = django_filters.MultipleChoiceFilter(field_name="category", lookup_expr="exact")
    price = django_filters.RangeFilter()
    date = django_filters.RangeFilter()
    # date__gt =django_filters.DateTimeFilter(field_name="Debut" , lookup_expr="gte")
    # date__lt = django_filters.DateTimeFilter(field_name="Fin",lookup_expr="lt") 
    
    class Meta:
        model = Product
        fields = {
              'title':['icontains'],
              'category__title':['exact'],
            #   'price':['lt','gte'],
            #   'date': ['lt','gte']
        }
                            
                
