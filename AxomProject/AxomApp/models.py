from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image as PILImage
import shutil
import io
import os
from django.core.files.base import ContentFile


from PIL import Image as PILImage


class ProductCategory(models.Model):
    product_category = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate slug if it's not already set
            base_slug = slugify(self.product_category)
            slug = base_slug
            counter = 1
            while ProductCategory.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_category



class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate slug if it's not already set
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Subcategory.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=100)
    product_description = models.TextField()
    watts = models.CharField(max_length=255)
    cct = models.CharField(max_length=255)
    dimmable_system = models.CharField(max_length=255)
    lumen_efficiency = models.CharField(max_length=255)
    fixing = models.CharField(max_length=255)
    led_source = models.CharField(max_length=255)
    ip_rating = models.CharField(max_length=255)
    life_span = models.CharField(max_length=255)
    image1 = models.ManyToManyField('Image', related_name='product_carousal_images')
    is_selected = models.BooleanField(default=False)
    displayimage1 = models.ImageField(upload_to='products/')
    displayimage2 = models.ImageField(upload_to='products/')
    displayimage3 = models.ImageField(upload_to='products/')
    email = models.EmailField()
    data_sheet = models.FileField(upload_to='product_files/')
    ldf_file = models.FileField(upload_to='product_files/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate slug if it's not already set
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Image(models.Model):
    file = models.ImageField(upload_to='product_carousal_images')

    def __str__(self):
        return str(self.file)

   

class ProductPage(models.Model):
    title = models.CharField(max_length=255)
    content=models.TextField()

    def __str__(self):
        return self.title

class Blog(models.Model):
        page_title = models.CharField(max_length=255)
        page_description = models.TextField()
        

        def __str__(self):
            return self.page_title 



class AddBlog(models.Model):
    blog_image = models.ImageField(upload_to='blog/')
    blog_image_caption = models.CharField(max_length=255)
    blog_description_title = models.TextField()
    blog_description = models.TextField()
    description_image = models.ImageField(upload_to='blog/')
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate slug if it's not already set
            base_slug = slugify(self.blog_description_title)
            slug = base_slug
            counter = 1
            while AddBlog.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        created_at_formatted = self.created_at.strftime("%d/%m/%y")
        updated_at_formatted = self.updated_at.strftime("%d/%m/%y")
        return f"{created_at_formatted} - {updated_at_formatted} - {self.blog_description_title}"



class Contact(models.Model):
        name = models.CharField(max_length=255)
        email = models.EmailField()
        phone = models.CharField(max_length=20)
        company = models.CharField(max_length=255)
        message = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.name


def upload_to(instance, filename):
    return f'Site_logo/{filename}'


class GeneralContent(models.Model):

    sitename = models.CharField(max_length=255, default="")
    slug = models.SlugField(max_length=255, unique=True)
    sitedescription = models.TextField()
    address1 = models.CharField(max_length=255, default=" ")
    address2 = models.CharField(max_length=255, default=" ")
    country = models.CharField(max_length=100, default=" ")
    city = models.CharField(max_length=255, default=" ")
    zipcode = models.CharField(max_length=20, default=" ")
    sitelogo = models.ImageField(upload_to='Site_logo/', blank=True)
    browsersitelogo = models.ImageField(upload_to=upload_to, blank=True)
    primaryemail = models.EmailField(default=" ")
    secondaryemail = models.EmailField(default=" ")
    replaytoemail = models.EmailField(default=" ")
    primarycontactnumber = models.CharField(max_length=20, default=" ")
    secondarycontactnumber = models.CharField(max_length=20, default=" ")
    tertiarycontactnumber = models.CharField(max_length=20, default=" ")
    facebookurl = models.CharField(max_length=255, default=" ")
    twitterurl = models.CharField(max_length=255, default=" ")
    instagramurl = models.CharField(max_length=255, default=" ")
    skypeurl = models.CharField(max_length=255, default=" ")
    linkedinurl = models.CharField(max_length=255, default=" ")
    metakeywords = models.CharField(max_length=255, default=" ")
    metadescription = models.CharField(max_length=50000, default=" ")
    googleanalyticscode = models.CharField(max_length=50000, default=" ")
    cssinput = models.CharField(max_length=255, default=" ")
    jsinput = models.CharField(max_length=255, default=" ")
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

 
   
    def save(self, *args, **kwargs):
        if self.browsersitelogo:
            img = PILImage.open(self.browsersitelogo)
            img = img.convert("RGBA")

            # Resize the image to a smaller size (32x32) before processing
            img = img.resize((32, 32), PILImage.BILINEAR)

            ico_data = io.BytesIO()
            img.save(ico_data, format="ICO")

            # Save the ICO data as a ContentFile to the browsersitelogo field
            self.browsersitelogo.save('favicon.ico', ContentFile(ico_data.getvalue()), save=False)

        if self.sitelogo:
            original_sitelogo = None
            
            try:
                # Check if the instance is being updated and get the original sitelogo
                original_instance = GeneralContent.objects.get(pk=self.pk)
                original_sitelogo = original_instance.sitelogo
            except GeneralContent.DoesNotExist:
                pass
        
        # If the sitelogo is new or different, rename it
            if original_sitelogo != self.sitelogo:
                # Delete the existing logo if it exists
                if original_sitelogo:
                    original_sitelogo.storage.delete(original_sitelogo.name)

                # Get the original filename and extension
                original_filename, extension = self.sitelogo.name.rsplit('.', 1)

                # Rename the image to 'logo.extension'
                new_filename = 'logo.' + extension
                self.sitelogo.name = 'Site_logo/' + new_filename


        super().save(*args, **kwargs)

    def __str__(self):
        return self.sitename




class Carousal(models.Model):
    title = models.CharField(max_length=100, default=" ")
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate slug if it's not already set
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Carousal.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title




class Home(models.Model):
    background_image = models.ImageField(upload_to='carousal_background_images/')
    title1 = models.CharField(max_length=255, default="")
    content11 = models.TextField()
    content12 = models.TextField()
    image1 = models.ImageField(upload_to='Home_Images/')
    

    title2=models.CharField(max_length=21, default="")
    content21=models.TextField(max_length=70)
    content22=models.TextField(max_length=70)
    image4=models.ImageField(upload_to='Home_Images/')
   

    title3=models.CharField(max_length=255, default="")
    content3=models.TextField()
    

    title4=models.CharField(max_length=255, default="")
    content41=models.TextField()
    content42=models.TextField()

    image8=models.ImageField(upload_to='Home_Images/')
    
    title5=models.CharField(max_length=21, default="")
    content51=models.TextField(max_length=70)
    content52=models.TextField(max_length=70)

    image11=models.ImageField(upload_to='Home_Images/')
   
  
        
    
    def __str__(self):
        return self.title1


class AboutUs(models.Model):
    title1=models.CharField(max_length=255,default="")
    content11=models.TextField()
    content12=models.TextField()
    image1=models.ImageField(upload_to='AboutUs_Images/')
    title2=models.CharField(max_length=255,default="")
    content2=models.TextField()
    title3=models.CharField(max_length=255,default="")
    content3=models.TextField()
    image4=models.ImageField(upload_to='AboutUs_Images/' )
    def __str__(self):
        return self.title1

class Download(models.Model):
    title = models.CharField(max_length=255,default="")
    content = models.TextField()
    image = models.ImageField(upload_to='download_images' )
    data_sheet = models.FileField(upload_to='download_files')

    def __str__(self):
        return self.title

class Sustainable(models.Model):
    title1 = models.CharField(max_length=255,default="")
    content11 = models.TextField()
    content12 = models.TextField()
    title2 =models.CharField(max_length=255,default="")
    content21 = models.TextField()
    content22 = models.TextField()
    image1=models.ImageField(upload_to='sustainable_images' )
    image2=models.ImageField(upload_to='sustainable_images' )
    def __str__(self):
        return self.title1
from django.db import models

class MapCoordinates(models.Model):
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='Contact_page_images', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.latitude is not None and self.longitude is not None:
            self.image = None
        elif self.image is not None:
            self.latitude = None
            self.longitude = None
        super().save(*args, **kwargs)


   
class Subscriber(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
   
class Dashboard_Subscriber(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


