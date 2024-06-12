from django.contrib import admin

from .models import Image,Subcategory,Subscriber,Dashboard_Subscriber,MapCoordinates,Carousal,Contact,GeneralContent,ProductPage,ProductCategory,AboutUs,Product,AddBlog,Download,Home,Blog,Sustainable
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Blog)
admin.site.register(GeneralContent)
admin.site.register(Carousal)
admin.site.register(ProductPage)
admin.site.register(Home)
admin.site.register(AboutUs)
admin.site.register(Download)
admin.site.register(ProductCategory)
admin.site.register(AddBlog)
admin.site.register(Subcategory)
admin.site.register(Sustainable)
admin.site.register(Image)
admin.site.register(MapCoordinates)

admin.site.register(Subscriber)
admin.site.register(Dashboard_Subscriber)
