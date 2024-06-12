from django.shortcuts import render, get_object_or_404, redirect
from .models import MapCoordinates
from django.http import Http404
from .models import Contact
from .models import Subcategory
from .models import Product, Image
from .models import Product
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .models import Carousal
from .models import Sustainable
from django.urls import reverse
from .models import GeneralContent, Contact
from .models import AddBlog
from .models import Product, Subcategory
from .models import ProductCategory
from .models import AboutUs, Blog, Download
from .models import AboutUs
from .models import Home
from .models import Carousal, Home
import os
from django.shortcuts import redirect
from django.http import HttpResponseServerError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.shortcuts import render, redirect
from .models import GeneralContent, AddBlog
from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth import logout
from django.contrib.sessions.models import Session

from django.contrib import messages
from .models import GeneralContent
from django.db import IntegrityError
from django.http import HttpResponseServerError, HttpResponse
from django.db import IntegrityError
from .models import GeneralContent, Subcategory, Product, Image, ProductCategory
from django.contrib import messages
from django.shortcuts import render, redirect
from PIL import Image as PILImage
import os
def compress_and_save_image(image, target_size_kb=1000):
    img = PILImage.open(image.path)

    # Convert the image to RGB mode (JPEG format)
    img = img.convert("RGB")

    # Determine the initial quality level
    quality = 85

    # Loop while the image size is larger than the target size
    while os.path.getsize(image.path) > target_size_kb * 1024 and quality >= 5:
        # Save the image with the current quality level
        img.save(image.path, format='JPEG', quality=quality, optimize=True)
        
        # Decrease the quality level for the next iteration
        quality -= 5




from datetime import timedelta
from django.utils import timezone



def index(request):
    try:
        obj = GeneralContent.objects.all()
        procat = ProductCategory.objects.filter(
            is_active=True)  # Fetch active product categories
        products = Product.objects.filter(subcategory__category__in=procat).order_by(
            '-created_at')  # Filter products based on active categories
        objs = Carousal.objects.all()
        bgimg = Home.objects.all()
        return render(request, 'index.html', {'obj': obj, 'objs': objs, 'bgimg': bgimg, 'products': products, 'procat': procat})
    except IntegrityError:
        return HttpResponse("Integrity Error occurred. Please try again later.")
    except Exception as e:
        return HttpResponseServerError(f"Internal Server Error: {e}")


def error_404_view(request, exception):
    obj = GeneralContent.objects.all()
    return render(request, '404.html', {'obj': obj})


def aboutus(request):
    try:
        obj = GeneralContent.objects.all()
        aboutus = AboutUs.objects.all()
        return render(request, 'about.html', {'obj': obj, 'aboutus': aboutus})
    except Exception as e:
        return HttpResponseServerError(f"Internal Server Error: {e}")


def product(request):
    try:
        obj = GeneralContent.objects.all()
        procat = ProductCategory.objects.all()
        subcategory = get_object_or_404(Subcategory, name="Downlights")
        pdt = Product.objects.filter(subcategory=subcategory).order_by('-id')
        paginator = Paginator(pdt, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'product.html', {'obj': obj, 'subcategory': subcategory, 'page_obj': page_obj, 'procat': procat, 'product': pdt})
    except Exception as e:
        return HttpResponseServerError(f"Internal Server Error: {e}")


def subcategory_details(request, slug):
    try:
        obj = GeneralContent.objects.all()
        subcategory = get_object_or_404(Subcategory, slug=slug)
        products = Product.objects.filter(subcategory=subcategory).order_by(
            '-id')  # Order products by -id
        product_category = subcategory.category  # Get the associated ProductCategory
        procat = ProductCategory.objects.all()
        paginator = Paginator(products, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'subcategory_details.html', {'subcategory': subcategory, 'products': page_obj, 'obj': obj, 'product_category': product_category, 'procat': procat})
    except Exception as e:

        return HttpResponseServerError(f"Internal Server Error: {e}")


def blog(request):
    try:
        obj = GeneralContent.objects.all()
        blogpage = Blog.objects.all()
        blog = AddBlog.objects.order_by('-id').all()
        paginator = Paginator(blog, 6) 

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'blog.html', {'obj': obj, 'page_obj': page_obj, 'blogpage': blogpage})
    except Exception as e:
        return HttpResponseServerError(f"Internal Server Error: {e}")


def contact(request):
    try:
        obj = GeneralContent.objects.all()
        
        return render(request, 'contact.html', {'obj': obj})
    except Exception as e:

        return HttpResponseServerError(f"Internal Server Error: {e}")


def sustainability(request):
    try:
        obj = GeneralContent.objects.all()
        sustain = Sustainable.objects.first()
        return render(request, 'sustainability.html', {'obj': obj, 'sustain': sustain})
    except Exception as e:

        return HttpResponseServerError(f"Internal Server Error: {e}")


def productdetail(request, slug):
    try:
        obj = GeneralContent.objects.all()
        product = get_object_or_404(Product, slug=slug)
        return render(request, 'product-details.html', {'obj': obj, 'product': product})
    except Exception as e:
        return HttpResponseServerError(f"Internal Server Error: {e}")


def blogdetail(request, slug):
    try:
        blog = AddBlog.objects.get(slug=slug)
        obj = GeneralContent.objects.all()
        return render(request, 'blog-details.html', {'obj': obj, 'blog': blog})
    except Exception as e:
        return HttpResponseServerError(f"Internal Server Error: {e}")


def download(request):
    try:
        obj = GeneralContent.objects.all()
        download = Download.objects.all()

        for item in download:
            print(item.data_sheet.url)

        return render(request, 'catalogue.html', {'obj': obj, 'download': download})
    except Exception as e:
        return HttpResponseServerError(f"Internal Server Error: {e}")


def login_form(request):
    obj=GeneralContent.objects.all()
    try:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            remember_me = request.POST.get('remember_me', False)

            user = auth.authenticate(
                request, username=username, password=password)

            if user is not None:
                auth.login(request, user)

                if remember_me:
                    request.session.set_expiry(30 * 24 * 60 * 60)  
                else:
                    request.session.set_expiry(60 * 60)  


                return redirect('dashboard')
            else:
                error_message = 'Invalid username/password'
                return render(request, 'login.html', {'error_message': error_message,'obj':obj})
        else:
            # Check if session has expired
            if request.session.get_expiry_age() <= 0:
                return render(request, 'login.html', {'error_message': 'Session has expired. Please log in again.', 'obj': obj})

            return render(request, 'login.html', {'obj': obj})
    except Exception as e:
        error_message = 'An error occurred: ' + str(e)
        return render(request, 'login.html', {'error_message': error_message, 'obj': obj})


def register_form(request):
    if request.method == 'POST':
        try:
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            username = request.POST['username']
            password = request.POST['password']
            confirmpassword = request.POST['Confirmpassword']
            email = request.POST['email']

            if password == confirmpassword:
                if User.objects.filter(username=username).exists():
                    error_message = 'Username is already taken. Please try again.'
                    return render(request, 'register.html', {'error_message': error_message})
                elif User.objects.filter(email=email).exists():
                    error_message = "This email has already been registered. Please try again."
                    return render(request, 'register.html', {'error_message': error_message})
                else:
                    tab = User.objects.create_user(
                        username=username, first_name=firstname, last_name=lastname, password=password, email=email)
                    tab.save()
                    return redirect('login_form')
            else:
                error_message = "Password verification failed. Please try again."
                return render(request, 'register.html', {'error_message': error_message})
        except KeyError as e:
            error_message = f"Missing required field: {e}"
            return render(request, 'register.html', {'error_message': error_message})
    else:

        return render(request, 'register.html')


def logout(request):
    try:
        auth.logout(request)
        return redirect(login_form)
    except Exception as e:

        error_message = 'An error occurred: ' + str(e)
        return render(request, 'logout.html', {'error_message': error_message})


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/passwordresetconfirm.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        if not form.is_valid():
            messages.error(
                self.request, 'Password reset failed. Please try again.')
            return render(self.request, self.template_name, {'form': form})

        # Render the 'confirmpassword.html' template
        return render(self.request, 'registration/passwordresetcomplete.html')


@login_required
def dashboard(request):
    total_count = ProductCategory.objects.count()
    subcategory_count = Subcategory.objects.count()
    product_count=Product.objects.count()
    blog_count = AddBlog.objects.count()
    enquiry_count= Contact.objects.count()
    subscriber_count =  Subscriber.objects.count()
    obj= GeneralContent.objects.all()
    return render(request, 'dashboard.html',{'total_count':total_count,'subcategory_count':subcategory_count,'product_count':product_count,'blog_count':blog_count,'enquiry_count':enquiry_count,'subscriber_count':subscriber_count,'obj':obj})


def generalcontent(request):
    try:
        obj = GeneralContent.objects.all()
        return render(request, 'generalcontent.html', {'obj': obj})
    except Exception as e:
        return HttpResponseServerError(f"Internal Server Error: {e}")


def site_primary_info(request):
    
    obj = GeneralContent.objects.all()

    try:
        content = GeneralContent.objects.get(pk=1)
    except GeneralContent.DoesNotExist:
        content = None
    except Exception as e:

        return HttpResponseServerError(f"Internal Server Error: {e}")

    if request.method == 'POST':
        try:
            content = GeneralContent.objects.get(
                pk=1) if content else GeneralContent()
            content.sitename = request.POST['sitename']
            content.sitedescription = request.POST['sitedescription']
            content.save()

            messages.success(
                request, 'The modifications have been successfully saved.')
            return redirect(site_primary_info)
        except Exception as e:

            return HttpResponseServerError(f"Internal Server Error: {e}")

    return render(request, 'primarylogo.html', {'general_content': content, 'obj': obj})


def site_address_info(request):
    
    
    obj = GeneralContent.objects.all()
    try:
        content = GeneralContent.objects.first()
    except GeneralContent.DoesNotExist:
        content = None
    except Exception as e:
        return HttpResponseServerError(f"Internal Server Error: {e}")

    if request.method == 'POST':
        try:
            address1 = request.POST.get('address1')
            address2 = request.POST.get('address2')
            country = request.POST.get('country')
            city = request.POST.get('city')
            zipcode = request.POST.get('zipcode')

            if address1 or country or city: 
                content = GeneralContent.objects.first() if content else GeneralContent()
                content.address1 = address1
                content.address2 = address2
                content.country = country
                content.city = city
                content.zipcode = zipcode
                content.save()
                messages.success(
                    request, 'The modifications have been successfully saved.')
                return redirect(site_address_info)
        except Exception as e:
            return HttpResponseServerError(f"Internal Server Error: {e}")

    return render(request, 'addressinfo.html', {'general_content': content, 'obj': obj})

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import GeneralContent
 # Import your image processing functions
#def convert_to_favicon(image_path, output_path):
  #  img = Image.open(image_path)
    
    # Resize the image to favicon dimensions (16x16)
   # img = img.resize((16, 16), Image.ANTIALIAS)
    
    # Save the image in .ico format
   # img.save(output_path, format='ICO')

def site_logo_favicon(request):
    obj = GeneralContent.objects.all()
    
    try:
        content = GeneralContent.objects.first()
    except GeneralContent.DoesNotExist:
        content = None
    except Exception as e:
        return render(request, 'error_page.html', {'error_message': f"Internal Server Error: {e}"}, status=500)

    if request.method == 'POST':
        try:
            content.sitelogo = request.FILES.get('sitelogo') or content.sitelogo
            content.browsersitelogo = request.FILES.get('browsersitelogo') or content.browsersitelogo
            content.save()

            if content.sitelogo:
                compress_and_save_image(content.sitelogo)

            messages.success(request, 'The modifications have been successfully saved.')
            return redirect('site_logo_favicon')
        except Exception as e:
            return redirect('site_logo_favicon')

    return render(request, 'primarylogo.html', {'general_content': content, 'obj': obj})


def contact_emails(request):
    
    obj = GeneralContent.objects.all()
    try:
        general_content = GeneralContent.objects.first()
    except GeneralContent.DoesNotExist:
        general_content = None
    except Exception as e:

        return HttpResponseServerError(f"Internal Server Error: {e}")

    if request.method == 'POST':
        try:
            primary_email = request.POST.get('primaryemail')
            secondary_email = request.POST.get('secondaryemail')
            replaytoemail = request.POST.get('replaytoemail')

            general_content.primaryemail = primary_email
            general_content.secondaryemail = secondary_email
            general_content.replaytoemail = replaytoemail
            general_content.save()
            messages.success(
                request, "The modifications have been successfully saved.")
            return redirect(contact_emails)
        except Exception as e:

            return HttpResponseServerError(f"Internal Server Error: {e}")

    return render(request, 'emailcontact.html', {'general_content': general_content, 'obj': obj})


def update_contact_numbers(request):
    
    obj = GeneralContent.objects.all()
    try:
        general_content = GeneralContent.objects.first()
    except GeneralContent.DoesNotExist:
        general_content = None
    except Exception as e:

        return HttpResponseServerError(f"Internal Server Error: {e}")

    if request.method == 'POST':
        try:
            primary_contact_number = request.POST.get('primary_contact_number')
            secondary_contact_number = request.POST.get(
                'secondary_contact_number')
            tertiary_contact_number = request.POST.get(
                'tertiary_contact_number')

            # Update the general content object
            general_content.primarycontactnumber = primary_contact_number
            general_content.secondarycontactnumber = secondary_contact_number
            general_content.tertiarycontactnumber = tertiary_contact_number
            general_content.save()
            messages.success(
                request, 'The changes have been saved successfully')
            return redirect(update_contact_numbers)
        except Exception as e:
          
            return HttpResponseServerError(f"Internal Server Error: {e}")

    return render(request, 'emailcontact.html', {'general_content': general_content, 'obj': obj})

# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponseServerError
from django.contrib import messages
from .models import GeneralContent  # Import your GeneralContent model here

def update_social_media_links(request):
    obj = GeneralContent.objects.all()
    try:
        general_content = GeneralContent.objects.first()
    except GeneralContent.DoesNotExist:
        general_content = None

    if request.method == 'POST':
        try:
            facebookurl = request.POST.get('facebookurl')
            twitterurl = request.POST.get('twitterurl')
            instagramurl = request.POST.get('instagramurl')
            skypeurl = request.POST.get('skypeurl')
            linkedinurl = request.POST.get('linkedinurl')

            if not general_content:
                general_content = GeneralContent()
            
            general_content.facebookurl = facebookurl
            general_content.twitterurl = twitterurl
            general_content.instagramurl = instagramurl
            general_content.skypeurl = skypeurl
            general_content.linkedinurl = linkedinurl

            general_content.save()
            messages.success(
                request, 'The modifications have been successfully saved.')
            return redirect('update_social_media_links')  # Use the correct URL name here
        except Exception as e:
            return HttpResponseServerError(f"Internal Server Error: {e}")

    return render(request, 'mediatags.html', {'general_content': general_content,'obj':obj})



def update_seotags(request):
    
    obj = GeneralContent.objects.all()
    try:
        general_content = get_object_or_404(GeneralContent, pk=1)
    except GeneralContent.DoesNotExist:
        general_content = None

    if request.method == 'POST':
        metakeywords = request.POST.get('metakeywords')
        metadescription = request.POST.get('metadescription')

        general_content.metakeywords = metakeywords
        general_content.metadescription = metadescription
        general_content.save()
        messages.success(
            request, "The modifications have been successfully saved.")
     
        return redirect('update_seotags')

    return render(request, 'mediatags.html', {'general_content': general_content, 'obj': obj})


def update_google_analytics(request):
    
    obj = GeneralContent.objects.all()
    try:
        general_content = GeneralContent.objects.first()
    except GeneralContent.DoesNotExist:
        general_content = None

    if request.method == 'POST':
        googleanalyticscode = request.POST.get('googleanalyticscode')

        general_content.googleanalyticscode = googleanalyticscode
        general_content.save()
        messages.success(
            request, "The modifications have been successfully saved.")
       
        return redirect('update_google_analytics')

    return render(request, 'googleanalytics_css.html', {'general_content': general_content, 'obj': obj})


def update_style(request):
    
   
    obj = GeneralContent.objects.first()  
    
    css_content = obj.cssinput if obj else ""
   
    js_content = obj.jsinput if obj else ""

 
    css_file_path = os.path.join(
        os.path.dirname(__file__),
        'static',
        'assets',
        'css',
        'custom.css'
    )
    js_file_path = os.path.join(
        os.path.dirname(__file__),
        'static',
        'assets',
        'js',
        'custom.js'
    )

  
    with open(css_file_path, 'w') as css_file:
        css_file.write(css_content)


    with open(js_file_path, 'w') as js_file:
        js_file.write(js_content)

    try:
        general_content = GeneralContent.objects.first()
    except GeneralContent.DoesNotExist:
        general_content = None

    if request.method == 'POST':
        cssinput = request.POST.get('cssinput')
        jsinput = request.POST.get('jsinput')

        general_content.cssinput = cssinput
        general_content.jsinput = jsinput
        general_content.save()

        messages.success(
            request, "The modifications have been successfully saved.")
  
        return redirect('update_style')

    return render(request, 'googleanalytics_css.html', {'general_content': general_content, 'obj': obj})


# pagecontent


def pagecontent(request):
    
    objs = Carousal.objects.all()
    homeobj = Home.objects.first()
    aboutusobj = AboutUs.objects.first()
    blogobj = Blog.objects.first()
    downloadobj = Download.objects.first()
    sustain = Sustainable.objects.first()
    map = MapCoordinates.objects.first()
    return render(request, 'pagecontent.html', {'objs': objs, 'map': map, 'homeobj': homeobj, 'aboutusobj': aboutusobj, 'blogobj': blogobj, 'downloadobj': downloadobj, 'sustain': sustain})


def create_carousal(request):
    
    obj = GeneralContent.objects.all()
    objs = Carousal.objects.all()
    template_name = 'carousalpagecontent.html'

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        obj = Carousal(title=title, content=content)
        obj.save()
        messages.success(
            request, 'You have successfully created a carousel')
        return redirect('create_carousal')

    return render(request, template_name, {'objs': objs,'obj':obj})


def carousal_list_table(request):
    
    obj = GeneralContent.objects.all()
    carousals = Carousal.objects.order_by('-id')
    paginator = Paginator(carousals, 15)  # Show 10 carousals per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'carousallistcontent.html', {'page_obj': page_obj,'obj':obj})


def delete_carousal(request, slug=None):
    
    try:
        carousal = Carousal.objects.get(slug=slug)
        carousal.delete()
       
        return redirect('carousal_list_table')
    except Carousal.DoesNotExist:
       
        return redirect('carousal_list_table')


def homepage(request):
    
    obj = GeneralContent.objects.all()
    try:
        homeobj = Home.objects.first()

        if request.method == 'POST':
           
            background_image = request.FILES.get('background_image')
            title1 = request.POST.get('title1')
            content11 = request.POST.get('content11')
            content12 = request.POST.get('content12')
            image1 = request.FILES.get('image1')

            title2 = request.POST.get('title2')
            content21 = request.POST.get('content21')
            content22 = request.POST.get('content22')
            image4 = request.FILES.get('image4')

            title3 = request.POST.get('title3')
            content3 = request.POST.get('content3')

            title4 = request.POST.get('title4')
            content41 = request.POST.get('content41')
            content42 = request.POST.get('content42')
            image8 = request.FILES.get('image8')

            title5 = request.POST.get('title5')
            content51 = request.POST.get('content51')
            content52 = request.POST.get('content52')
            image11 = request.FILES.get('image11')

            if homeobj:
              
                homeobj.background_image = background_image or homeobj.background_image
            else:
               
                homeobj = Home(background_image=background_image)

           
            homeobj.title1 = title1
            homeobj.content11 = content11
            homeobj.content12 = content12
            homeobj.image1 = image1 or homeobj.image1

            homeobj.title2 = title2
            homeobj.content21 = content21
            homeobj.content22 = content22
            homeobj.image4 = image4 or homeobj.image4

            homeobj.title3 = title3
            homeobj.content3 = content3

            homeobj.title4 = title4
            homeobj.content41 = content41
            homeobj.content42 = content42
            homeobj.image8 = image8 or homeobj.image8

            homeobj.title5 = title5
            homeobj.content51 = content51
            homeobj.content52 = content52
            homeobj.image11 = image11 or homeobj.image11

            homeobj.save()

            
            compress_and_save_image(homeobj.background_image)
            compress_and_save_image(homeobj.image1)
            compress_and_save_image(homeobj.image4)
            compress_and_save_image(homeobj.image8)
            compress_and_save_image(homeobj.image11)

            messages.success(
                request, 'The modifications have been successfully saved.')

            return redirect('homepage')

        context = {
            'homeobj': homeobj,'obj':obj
        }
        return render(request, 'homepagecontent.html', context)
    except Exception as e:
        messages.error(request, f'Failed to update the Home Page: {str(e)}')
        return redirect('homepage')


def About_Us(request):
    
    obj=GeneralContent.objects.all()
    try:
        aboutusobj = AboutUs.objects.first()
    except AboutUs.DoesNotExist:
        aboutusobj = None

    if request.method == 'POST':
     
        title1 = request.POST.get('title1')
        content11 = request.POST.get('content11')
        content12 = request.POST.get('content12')
        image1 = request.FILES.get('image1')

        title2 = request.POST.get('title2')
        content2 = request.POST.get('content2')
        image4 = request.FILES.get('image4')
        title3 = request.POST.get('title3')
        content3 = request.POST.get('content3')

        try:
            if aboutusobj:
            
                aboutusobj.title1 = title1
                aboutusobj.content11 = content11
                aboutusobj.content12 = content12
                aboutusobj.image1 = image1 or aboutusobj.image1
                aboutusobj.title2 = title2
                aboutusobj.content2 = content2
                aboutusobj.image4 = image4 or aboutusobj.image4
                aboutusobj.title3 = title3
                aboutusobj.content3 = content3
                aboutusobj.save()
                compress_and_save_image(aboutusobj.image1)
                compress_and_save_image(aboutusobj.image4)
                messages.success(
                    request, 'The modifications have been successfully saved.')
            else:
        
                aboutusobj = AboutUs.objects.create(
                    title1=title1,
                    content11=content11,
                    content12=content12,
                    image1=image1,
                    title2=title2,
                    content2=content2,
                    image4=image4,
                    title3=title3,
                    content3=content3,
                )
                compress_and_save_image(aboutusobj.image1)
                compress_and_save_image(aboutusobj.image4)
                messages.success(
                    request, 'The modifications have been successfully saved.')
        except Exception as e:
            messages.error(request, str(e))

        return redirect('About_Us')

    return render(request, 'aboutuspagecontent.html', {'aboutusobj': aboutusobj,'obj':obj})


def blog_Page(request):
    
    obj = GeneralContent.objects.all()
    try:
        blogobj = Blog.objects.get()  
    except Blog.DoesNotExist:
        blogobj = None

    if request.method == 'POST':
        page_title = request.POST.get('page_title')
        page_description = request.POST.get('page_description')

        try:
            if blogobj:
                blogobj.page_title = page_title
                blogobj.page_description = page_description
                blogobj.save()
                messages.success(
                    request, 'The modifications have been successfully saved.')
                return redirect('blog_Page')
            else:
                blogobj = Blog.objects.create(
                    page_title=page_title, page_description=page_description)
                messages.success(
                    request, 'You have successfully created a new blog page.')
                return redirect('blog_Page')
        except Exception as e:
            messages.error(request, str(e))

    return render(request, 'blogpagecontent.html', {'blogobj': blogobj,'obj':obj})


def Download_Page(request):
    
    obj = GeneralContent.objects.all()
    try:
        downloadobj = Download.objects.first()
    except Download.DoesNotExist:
        downloadobj = None

    if request.method == 'POST':
        # Retrieve the form data
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        data_sheet = request.FILES.get('data_sheet')

        try:
            if downloadobj:
                # An existing object is found, update it with the new data
                downloadobj.title = title
                downloadobj.content = content
                if image:
                    downloadobj.image = image or downloadobj.image
                if data_sheet:
                    downloadobj.data_sheet = data_sheet
                downloadobj.save()
                compress_and_save_image(downloadobj.image)
                messages.success(
                    request, 'The modifications have been successfully saved.')
            else:
                # No existing object found, create a new one with the provided data
                new_downloadobj = Download(title=title, content=content)
                if image:
                    new_downloadobj.image = image
                if data_sheet:
                    new_downloadobj.data_sheet = data_sheet
                new_downloadobj.save()
                compress_and_save_image(new_downloadobj.image)
              
                messages.success(
                    request, 'The content for the download page has been successfully created.')
        except Exception as e:
            messages.error(request, str(e))

        return redirect('Download_Page')

    return render(request, 'downloadpagecontent.html', {'downloadobj': downloadobj,'obj':obj})


def product_category(request):
    
    obj = GeneralContent.objects.all()
    if request.method == 'POST':
        product_category = request.POST['product_category']

        try:
            categoryobj = ProductCategory(product_category=product_category)
            categoryobj.save()
            messages.success(
                request, 'You have completed your task successfully')
            return redirect('product_category')
        except IntegrityError:
            error_message = 'An integrity error occurred while saving your content.'
            messages.error(request, error_message)
            return redirect('product_category')
        except Exception as e:
            error_message = 'An internal server error occurred.'
            messages.error(request, error_message)
            return redirect('product_category')

    categories = ProductCategory.objects.all()
    return render(request, 'categorycontent.html', {'categories': categories,'obj':obj})


def update_category(request, slug):
    
    obj = GeneralContent.objects.all()
    categoryobj = get_object_or_404(ProductCategory, slug=slug)

    if request.method == 'POST':
        categoryobj.product_category = request.POST.get('product_category')
        try:
            categoryobj.save()
            messages.success(
                request, 'Category has been successfully modified.')
        except IntegrityError:
            messages.error(
                request, 'Category update failed due to integrity error')
        return redirect('update_category' , slug=categoryobj.slug)

    return render(request, 'updatecategorycontent.html', {'categoryobj': categoryobj,'obj':obj})


def category_list_table(request):
    
    obj = GeneralContent.objects.all()
    categories = ProductCategory.objects.all().order_by('-id')
    total_count = categories.count()
    paginator = Paginator(categories, 10)  # Show 10 categories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'categorylistcontent.html', {'page_obj': page_obj,' total_count': total_count,'obj':obj})


def delete_category(request, slug):
    try:
        category = get_object_or_404(ProductCategory, slug=slug)
        category.delete()

    except ProductCategory.DoesNotExist:
        messages.error(request, 'Category does not exist')
    return redirect('category_list_table')

from PIL import Image as PILImage
import os


def resize_and_compress_image(image, target_width=832, target_height=829):
    img = PILImage.open(image)
    img = img.resize((target_width, target_height), PILImage.LANCZOS)
    img.save(image.path, format='JPEG', quality=100)  # You can adjust the format and quality as needed
    compress_and_save_image(image)

def resize_and_compress_image_blog(image, target_width=1386, target_height=1176):
    img = PILImage.open(image)
    img = img.resize((target_width, target_height), PILImage.ANTIALIAS)
    img.save(image.path, format='JPEG', quality=100)  # You can adjust the format and quality as needed
    compress_and_save_image(image)
from django.core.files.storage import default_storage
from django.conf import settings

def product_page(request):
    
    obj = GeneralContent.objects.all()
    if request.method == 'POST':
        try:
            # Retrieve form data from request.POST dictionary
            title = request.POST.get('title')
            subcategory_id = request.POST.get('subcategory')
            model_name = request.POST.get('model_name')
            watts = request.POST.get('watts')
            cct = request.POST.get('cct')
            dimmable_system = request.POST.get('dimmable_system')
            lumen_efficiency = request.POST.get('lumen_efficiency')
            fixing = request.POST.get('fixing')
            led_source = request.POST.get('led_source')
            ip_rating = request.POST.get('ip_rating')
            life_span = request.POST.get('life_span')
            product_description = request.POST.get('product_description')
            image_files = request.FILES.getlist('image1[]')
            selected_image_filename = request.POST.get('selected-image-filename')
            displayimage2 = request.FILES.get('displayimage2')
            displayimage3 = request.FILES.get('displayimage3')
            data_sheet = request.FILES.get('data_sheet')
            ldf_file = request.FILES.get('ldf_file')

            # Create a new Product instance
            product = Product(
                title=title,
                subcategory_id=subcategory_id,
                model_name=model_name,
                watts=watts,
                cct=cct,
                dimmable_system=dimmable_system,
                lumen_efficiency=lumen_efficiency,
                fixing=fixing,
                led_source=led_source,
                ip_rating=ip_rating,
                life_span=life_span,
                product_description=product_description,
                displayimage1=selected_image_filename,
                displayimage2=displayimage2,
                displayimage3=displayimage3,
                data_sheet=data_sheet,
                ldf_file=ldf_file,
            )
            product.save()  # Save the product instance to the database

            # Add the carousel images to the product
            for image_file in image_files:
                image = Image(file=image_file)
                image.save()
                product.image1.add(image)

            selected_image_file = None

            for image_file in image_files:
                if image_file.name == selected_image_filename:
                    selected_image_file = image_file
                    break

            if selected_image_file:
                    base_dir = os.path.join(settings.MEDIA_ROOT, 'Product', product.title)
                    os.makedirs(base_dir, exist_ok=True)  # Create the directory if it doesn't exist

                    # Use a unique filename to avoid potential conflicts
                    unique_filename = f"{product.title}_{selected_image_filename}"
                    
                    # Construct the relative path within the media root
                    relative_image_path = os.path.join('Product', product.title, unique_filename)

                    # Save the image to the relative path
                    image_path = default_storage.save(relative_image_path, selected_image_file)

                    # Update the displayimage1 field with the saved image path
                    product.displayimage1 = image_path
                    product.save()

                    # Process and optimize the image
                    resize_and_compress_image(product.displayimage1)

                            

            # Optimize and compress the display images
        

            messages.success(request, 'Product has been successfully created.')
            return redirect('product_page')
        except IntegrityError:
            messages.error(request, 'An integrity error occurred while saving your content')
        except Exception as e:
            messages.error(request, f'Failed to add the product: {str(e)}')

    subcategories = Subcategory.objects.all()
    procat = ProductCategory.objects.filter(is_active=True)
    return render(request, 'productcontent.html', {'subcategories': subcategories, 'procat': procat, 'obj': obj})







from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import Product

def product_list(request):
    
    obj = GeneralContent.objects.all()
    products = Product.objects.order_by('-id')
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Handle POST request to update is_selected for a product
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        is_selected = request.POST.get('is_selected', False)
        product = get_object_or_404(Product, pk=product_id)
        product.is_selected = bool(is_selected)
        product.save()
        return JsonResponse({'status': 'success', 'message': 'is_selected updated successfully'})
    
    return render(request, 'productlistcontent.html', {'page_obj': page_obj,'obj':obj})



def delete_product(request, slug=None):
    try:
        product = get_object_or_404(Product, slug=slug)
        product.delete()

    except Product.DoesNotExist:
        messages.error(request, 'Product does not exist')
    return redirect('product_list')
import os
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import GeneralContent, Product, Image, Subcategory, ProductCategory


def update_product(request, slug=None):
    obj = GeneralContent.objects.all()

    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        messages.error(request, 'Product does not exist')
        return redirect('product_list')

    # Fetch only active product categories
    procat = ProductCategory.objects.filter(is_active=True)

    if request.method == 'POST':
        try:
            # Retrieve form data from request.POST dictionary
            title = request.POST.get('title')
            subcategory_id = request.POST.get('subcategory')
            model_name = request.POST.get('model_name')
            watts = request.POST.get('watts')
            cct = request.POST.get('cct')
            dimmable_system = request.POST.get('dimmable_system')
            lumen_efficiency = request.POST.get('lumen_efficiency')
            fixing = request.POST.get('fixing')
            led_source = request.POST.get('led_source')
            ip_rating = request.POST.get('ip_rating')
            life_span = request.POST.get('life_span')
            product_description = request.POST.get('product_description')
            image_files = request.FILES.getlist('image1[]')
            selected_image_filename = request.POST.get('selected-image-filename')
            displayimage2 = request.FILES.get('displayimage2')
            displayimage3 = request.FILES.get('displayimage3')
            data_sheet = request.FILES.get('data_sheet')
            ldf_file = request.FILES.get('ldf_file')

            # Update the product instance
            product.title = title
            product.subcategory_id = subcategory_id
            product.model_name = model_name
            product.watts = watts
            product.cct = cct
            product.dimmable_system = dimmable_system
            product.lumen_efficiency = lumen_efficiency
            product.fixing = fixing
            product.led_source = led_source
            product.ip_rating = ip_rating
            product.life_span = life_span
            product.product_description = product_description

            # Clear and update image1 field if new images are provided
            if image_files:
                # Clear existing images
                product.image1.clear()
                for image_file in image_files:
                    image = Image(file=image_file)
                    image.save()
                    product.image1.add(image)
                    
            selected_image_file = None
            for image_file in image_files:
                if image_file.name == selected_image_filename:
                    selected_image_file = image_file
                    break

            if selected_image_file:
                base_dir = os.path.join(settings.MEDIA_ROOT, 'Product', product.title)
                os.makedirs(base_dir, exist_ok=True)  # Create the directory if it doesn't exist

                # Use a unique filename to avoid potential conflicts
                unique_filename = f"{product.title}_{selected_image_filename}"
                
                # Construct the relative path within the media root
                relative_image_path = os.path.join('Product', product.title, unique_filename)

                # Save the image to the relative path
                image_path = default_storage.save(relative_image_path, selected_image_file)

                # Update the displayimage1 field with the saved image path
                product.displayimage1 = image_path

                # Process and optimize the image
                resize_and_compress_image(product.displayimage1)

            # Update display images if new files are provided
            if displayimage2:
                product.displayimage2 = displayimage2
                
            if displayimage3:
                product.displayimage3 = displayimage3

            # Update data sheet and LDT file if new files are provided
            if data_sheet:
                product.data_sheet = data_sheet
            if ldf_file:
                product.ldf_file = ldf_file

            product.save()  # Save the updated product instance to the database

            # Optimize and compress the display images
            for display_image_field in ['displayimage1', 'displayimage2', 'displayimage3']:
                display_image = getattr(product, display_image_field)
                if display_image:
                    resize_and_compress_image(display_image)

            messages.success(request, 'The modifications have been successfully saved.')
            return redirect('update_product', slug=product.slug)
        except Exception as e:
            messages.error(request, f'Error updating product: {str(e)}')

    subcategories = Subcategory.objects.all()
    products = Product.objects.all()

    # Fetch the image URLs for each product
    image_urls = [image.file.url for product_obj in products for image in product_obj.image1.all()]

    return render(request, 'updateproductcontent.html', {'subcategories': subcategories, 'product': product, 'image_urls': image_urls, 'procat': procat, 'obj': obj})






def addblog(request):
    
    obj = GeneralContent.objects.all()
    if request.method == 'POST':
        try:
            blog_image = request.FILES.get('blog_image')
            blog_image_caption = request.POST['blog_image_caption']
            blog_description_title = request.POST['blog_description_title']
            blog_description = request.POST['blog_description']
            description_image = request.FILES.get('description_image')

            addblogobj = AddBlog(
                blog_image=blog_image,
                blog_image_caption=blog_image_caption,
                blog_description_title=blog_description_title,
                blog_description=blog_description,
                description_image=description_image
            )

            addblogobj.save()
            resize_and_compress_image_blog(addblogobj.blog_image)
            compress_and_save_image(addblogobj.description_image)
            messages.success(
                request, 'A new blog has been successfully saved.')

            return redirect('addblog')
        except Exception:
            pass

    return render(request, 'blogcontent.html', {'addblogobj': None,'obj':obj})


def update_blog(request, slug):
    
    obj = GeneralContent.objects.all()
    try:
        blog = AddBlog.objects.get(slug=slug)

        if request.method == 'POST':
            try:
                blog_image = request.FILES.get('blog_image')
                blog_image_caption = request.POST['blog_image_caption']
                blog_description_title = request.POST['blog_description_title']
                blog_description = request.POST['blog_description']
                description_image = request.FILES.get('description_image')

                # Update the blog object with the new data
                blog.blog_image = blog_image or blog.blog_image
                blog.blog_image_caption = blog_image_caption
                blog.blog_description_title = blog_description_title
                blog.blog_description = blog_description
                blog.description_image = description_image or blog.description_image

                # Save the updated blog object to the database
                blog.save()
                resize_and_compress_image_blog(blog.blog_image)
                compress_and_save_image(blog.description_image)
                messages.success(
                    request, 'The modifications have been successfully saved.')

                return redirect('update_blog')
            except Exception:
                pass

        return render(request, 'updateblogcontent.html', {'blog': blog,'obj':obj})
    except AddBlog.DoesNotExist:
        messages.error(request, '')
        return redirect('blog_list')


def blog_list(request):
    
    obj = GeneralContent.objects.all()
    blogs = AddBlog.objects.order_by('-id')
    paginator = Paginator(blogs, 20)  # Show 15 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'bloglistcontent.html', {'page_obj': page_obj,'obj':obj})


def delete_blog(request, slug):
    try:
        blog = AddBlog.objects.get(slug=slug)
        blog.delete()

    except AddBlog.DoesNotExist:
        messages.error(request, 'The blog you requested does not exist')

    return redirect('blog_list')
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import GeneralContent, MapCoordinates, Contact
from django.core.mail import send_mail
from django.conf import settings

def contains_letter(s):
    return any(c.isalpha() for c in s)
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import GeneralContent, Contact  # Import your models here

def contactus(request):
    obj = GeneralContent.objects.all()

    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            company = request.POST.get('company')
            message = request.POST.get('message')

            # Validate name, company, and message fields
            if not name.isalpha():
                messages.error(request, 'Please kindly provide a valid name. Thank you.')
                return redirect('contactus')

            if not contains_letter(company):
                messages.error(request, 'Please ensure that you have mentioned your subject. Thank you.')
                return redirect('contactus')

            if not contains_letter(message):
                messages.error(request, 'Please ensure that you have mentioned your message. Thank you.')
                return redirect('contactus')

            # Validate phone number contains only digits
            if not phone.isdigit():
                messages.error(request, 'Kindly ensure accurate and proper entry of your phone number. Thank you.')
                return redirect('contactus')

            # Validate phone number length
            if len(phone) > 12:
                messages.error(request, 'Kindly ensure accurate and proper entry of your phone number. Thank you..')
                return redirect('contactus')

            # All validations passed, create the contact object
            contactusobj = Contact.objects.create(
                name=name,
                email=email,
                company=company,
                phone=phone,
                message=message
            )

            if contactusobj:
                messages.success(request, 'Your enquiry has been registered. We will get back to you soon.')
                # Sending email to the host
                subject = 'New Enquiry Received'
                message = f'You have received a new enquiry from {name}. Please check the admin panel.'
                email_from = f'Axom Lights <{settings.EMAIL_HOST_USER}>'

                general_content_instance = obj.first()  # Assuming you retrieve a single instance
                if general_content_instance:
                    email_to = [general_content_instance.replaytoemail]
                    send_mail(subject, message, email_from, email_to, fail_silently=False)
                else:
                    messages.error(request, 'Failed to retrieve contact information for sending email.')
            else:
                messages.error(request, 'Sorry, your enquiry has not been registered. Please try again.')
        except Exception as e:
            messages.error(request, f'Failed to register the enquiry: {str(e)}')

        return redirect('contactus')  # Redirect after successful POST

    # Filter messages specific to 'contactus' page
    contactus_messages = [message for message in messages.get_messages(
        request) if message.tags == 'success' or message.tags == 'error']

    return render(request, 'contact.html', {'obj': obj, 'contactus_messages': contactus_messages})



def contact_us_list(request):
    
    obj = GeneralContent.objects.all()
    contact = Contact.objects.order_by('-id')
    paginator = Paginator(contact, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'contactenquirytable.html', {'page_obj': page_obj,'obj':obj})


def sub_category(request):
    
    obj = GeneralContent.objects.all()
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            description = request.POST.get('description')
            category_id = request.POST.get('category')
            category = ProductCategory.objects.get(id=category_id)

            # Check if a subcategory with the same name already exists
            if Subcategory.objects.filter(name=name).exists():
                error_message = f"A subcategory with the name '{name}' already exists."
                messages.error(request, error_message)
                return redirect('sub_category')
            else:
                subcategory = Subcategory(
                    name=name, description=description, category=category)
                subcategory.save()
                messages.success(
                    request, 'You have successfully created a subcategory.')
            return HttpResponseRedirect(reverse('sub_category'))
        except Exception as e:
            messages.error(
                request, f'Failed to create the subcategory: {str(e)}')
            return HttpResponseRedirect(reverse('sub_category'))

    categories = ProductCategory.objects.all()
    return render(request, 'subcategorycontent.html', {'categories': categories,'obj':obj})


def subcategory_list_table(request):
    
    obj = GeneralContent.objects.all()
    procat = ProductCategory.objects.filter(is_active=True)
    subcategories = Subcategory.objects.select_related(
        'category').order_by('-id')
    paginator = Paginator(subcategories, 10)  # Show 10 subcategories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'subcategorylistcontent.html', {'page_obj': page_obj, 'procat': procat,'obj':obj})


def delete_subcategory(request, slug):
    
    try:
        subcategory = get_object_or_404(Subcategory, slug=slug)
        subcategory.delete()

    except Subcategory.DoesNotExist:
        messages.error(request, 'The subcategory you requested does not exist')

    return redirect('subcategory_list_table')


def update_sub_category(request, slug=None):
    
    obj = GeneralContent.objects.all()
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            description = request.POST.get('description')
            category_id = request.POST.get('category')
            # Use category_id instead of slug
            category = get_object_or_404(ProductCategory, slug=category_id)

            if slug:  # Update existing subcategory
                subcategory = get_object_or_404(Subcategory, slug=slug)
                subcategory.name = name
                subcategory.description = description
                subcategory.category = category
                subcategory.save()
            else:  # Create new subcategory
                subcategory = Subcategory(
                    name=name, description=description, category=category)
                subcategory.save()
                messages.success(request,'Subcategory has been successfully modified')

            return redirect('update_sub_category' , slug=subcategory.slug)

        categories = ProductCategory.objects.all()
        subcategory = None

        if slug:  # Fetch the existing subcategory for editing
            subcategory = get_object_or_404(Subcategory, slug=slug)

        return render(request, 'updatesubcategorycontent.html', {'categories': categories, 'subcategory': subcategory,'obj':obj})
    except Exception as e:
        messages.error(request, f'Failed to update the subcategory: {str(e)}')
        return redirect('update_sub_category' , slug=subcategory.slug)

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Sustainable

def update_sustainability_content(request):
    
    obj = GeneralContent.objects.all()
    try:
        sustainability_content = Sustainable.objects.first()
    except Sustainable.DoesNotExist:
        sustainability_content = None

    if request.method == 'POST':
        title1 = request.POST.get('title1')
        content11 = request.POST.get('content11')
        content12 = request.POST.get('content12')
        title2 = request.POST.get('title2')
        content21 = request.POST.get('content21')
        content22 = request.POST.get('content22')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')

        if sustainability_content:
            # Update existing sustainability content
            sustainability_content.title1 = title1
            sustainability_content.content11 = content11
            sustainability_content.content12 = content12
            sustainability_content.title2 = title2
            sustainability_content.content21 = content21
            sustainability_content.content22 = content22

            if image1:
                sustainability_content.image1 = image1
            if image2:
                sustainability_content.image2 = image2

            sustainability_content.save()
            compress_and_save_image(sustainability_content.image1)
            compress_and_save_image(sustainability_content.image2)
            messages.success(request, 'The modifications have been successfully saved.')
        else:
            # Create new sustainability content
            sustainability_content = Sustainable(
                title1=title1,
                content11=content11,
                content12=content12,
                title2=title2,
                content21=content21,
                content22=content22,
                image1=image1,
                image2=image2
            )
            sustainability_content.save()
            compress_and_save_image(sustainability_content.image1)
            compress_and_save_image(sustainability_content.image2)
            messages.success(request, 'The page content has been successfully created.')

        return redirect('update_sustainability_content')

    return render(request, 'sustainabilitycontent.html', {'sustain': sustainability_content,'obj':obj})


from django.shortcuts import get_object_or_404, redirect, render
from .models import Carousal

def update_carousal(request, slug):
    
    obj = GeneralContent.objects.all()
    template_name = 'updatecarousalcontent.html'
    carousal = get_object_or_404(Carousal, slug=slug)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        carousal.title = title
        carousal.content = content
        carousal.save()
        messages.success(request,'Carousal has been successfully modified')

        # Redirect back to the updated carousel's detail page
        return redirect('update_carousal', slug=carousal.slug)

    return render(request, template_name, {'carousal': carousal,'obj':obj})


def toggle_category(request, category_id):
    category = get_object_or_404(ProductCategory, id=category_id)
    category.is_active = not category.is_active
    category.save()
    return redirect('category_list_table')


def map_view(request):
    
    map_coordinates = MapCoordinates.objects.first()
    latitude = map_coordinates.latitude
    longitude = map_coordinates.longitude

    if latitude is None or longitude is None:
        # Set default latitude and longitude values
        latitude = 0.0
        longitude = 0.0

    return render(request, 'contact.html', {'latitude': latitude, 'longitude': longitude})

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from .models import MapCoordinates, GeneralContent

def map_input(request):
    
    template_name = 'contactpagecontent.html'
    obj = GeneralContent.objects.all()

    try:
        # Retrieve the existing MapCoordinates object or create a new one
        map_coordinates, created = MapCoordinates.objects.get_or_create(pk=1)
    except MapCoordinates.DoesNotExist:
        # Create a new MapCoordinates object if it doesn't exist
        map_coordinates = MapCoordinates()

    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        image = request.FILES.get('image')

        if (latitude and longitude) or image:
            if latitude and longitude:
                map_coordinates.latitude = latitude
                map_coordinates.longitude = longitude
                map_coordinates.image = None
            elif image:
                map_coordinates.image = image
                map_coordinates.latitude = None
                map_coordinates.longitude = None

            try:
                map_coordinates.save()
                
            
                messages.success(request, 'Your fields have been successfully updated.')
                return redirect('map_input')
            except (ValueError, IntegrityError):
                messages.error(request, "An error occurred while saving the fields.")
        else:
            messages.error(request, "Invalid combination of fields. Please provide either latitude and longitude or an image.")

    
    context = {
        'map': map_coordinates,
        'obj': obj,
    }
    return render(request, template_name, {'obj': obj, **context})

from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags
from .models import Subscriber

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Subscriber
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Subscriber
from django.core.mail import EmailMessage

def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Save the email to the database
            subscriber, created = Subscriber.objects.get_or_create(email=email)

            # Send a confirmation email to the subscriber
            email_subject_subscriber = 'Newsletter Subscription Confirmation'
            email_message_subscriber = 'Dear Subscriber,\nCongratulations! You have successfully subscribed to our newsletter.'
            email_from = f'Axom Lights <{settings.EMAIL_HOST_USER}>'
            email_to_subscriber = [email]
            email_subscriber = EmailMessage(
                email_subject_subscriber,
                email_message_subscriber,
                email_from,
                email_to_subscriber
            )
            email_subscriber.send()

            # Retrieve the replaytoemail value from the GeneralContent instance
            general_content_instance = GeneralContent.objects.first()  # Assuming you retrieve a single instance
            if general_content_instance:
                email_to = [general_content_instance.replaytoemail]

                # Send a notification email to the EMAIL_HOST_USER
                email_subject_host = 'New Newsletter Subscription'
                email_message_host = f'A new subscription has been made. Email: {email}'
                email_from_host = f'Axom Lights <{settings.EMAIL_HOST_USER}>'
                email_to_host = [general_content_instance.replaytoemail]
                email_host = EmailMessage(
                    email_subject_host,
                    email_message_host,
                    email_from_host,
                    email_to_host
                )
                email_host.send()
            

            # Save the subscriber object to the database
            subscriber.save()

            return redirect('index')

    return redirect('index')



def about_subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Save the email to the database
            subscriber, created = Subscriber.objects.get_or_create(email=email)

            # Send a confirmation email to the subscriber
            email_subject_subscriber = 'Newsletter Subscription Confirmation'
            email_message_subscriber = 'Dear Subscriber,\nCongratulations! You have successfully subscribed to our newsletter.'
            email_from = f'Axom Lights <{settings.EMAIL_HOST_USER}>'
            email_to_subscriber = [email]
            email_subscriber = EmailMessage(
                email_subject_subscriber,
                email_message_subscriber,
                email_from,
                email_to_subscriber
            )
            email_subscriber.send()

            # Retrieve the replaytoemail value from the GeneralContent instance
            general_content_instance = GeneralContent.objects.first()  # Assuming you retrieve a single instance
            if general_content_instance:
                email_to = [general_content_instance.replaytoemail]

                # Send a notification email to the EMAIL_HOST_USER
                email_subject_host = 'New Newsletter Subscription'
                email_message_host = f'A new subscription has been made. Email: {email}'
                email_from_host = f'Axom Lights <{settings.EMAIL_HOST_USER}>'
                email_to_host = [general_content_instance.replaytoemail]
                email_host = EmailMessage(
                    email_subject_host,
                    email_message_host,
                    email_from_host,
                    email_to_host
                )
                email_host.send()
            
            # Save the subscriber object to the database
            subscriber.save()


            return redirect('aboutus')

    return redirect('aboutus')

def product_subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Save the email to the database
            subscriber, created = Subscriber.objects.get_or_create(email=email)

            # Send a confirmation email to the subscriber
            email_subject_subscriber = 'Newsletter Subscription Confirmation'
            email_message_subscriber = 'Dear Subscriber,\nCongratulations! You have successfully subscribed to our newsletter.'
            email_from = f'Axom Lights <{settings.EMAIL_HOST_USER}>'
            email_to_subscriber = [email]
            email_subscriber = EmailMessage(
                email_subject_subscriber,
                email_message_subscriber,
                email_from,
                email_to_subscriber
            )
            email_subscriber.send()

            # Retrieve the replaytoemail value from the GeneralContent instance
            general_content_instance = GeneralContent.objects.first()  # Assuming you retrieve a single instance
            if general_content_instance:
                email_to = [general_content_instance.replaytoemail]

                # Send a notification email to the EMAIL_HOST_USER
                email_subject_host = 'New Newsletter Subscription'
                email_message_host = f'A new subscription has been made. Email: {email}'
                email_from_host = f'Axom Lights <{settings.EMAIL_HOST_USER}>'
                email_to_host = [general_content_instance.replaytoemail]
                email_host = EmailMessage(
                    email_subject_host,
                    email_message_host,
                    email_from_host,
                    email_to_host
                )
                email_host.send()
            
            # Save the subscriber object to the database
            subscriber.save()


            return redirect('product')

    return redirect('product')

def blog_subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Save the email to the database
            subscriber, created = Subscriber.objects.get_or_create(email=email)

            # Send a confirmation email to the subscriber
            email_subject_subscriber = 'Newsletter Subscription Confirmation'
            email_message_subscriber = 'Dear Subscriber,\nCongratulations! You have successfully subscribed to our newsletter.'
            email_from = f'Axom Lights <{settings.EMAIL_HOST_USER}>'
            email_to_subscriber = [email]
            email_subscriber = EmailMessage(
                email_subject_subscriber,
                email_message_subscriber,
                email_from,
                email_to_subscriber
            )
            email_subscriber.send()

            # Retrieve the replaytoemail value from the GeneralContent instance
            general_content_instance = GeneralContent.objects.first()  # Assuming you retrieve a single instance
            if general_content_instance:
                email_to = [general_content_instance.replaytoemail]

                # Send a notification email to the EMAIL_HOST_USER
                email_subject_host = 'New Newsletter Subscription'
                email_message_host = f'A new subscription has been made. Email: {email}'
                email_from_host = f'Axom Lights <{settings.EMAIL_HOST_USER}>'
                email_to_host = [general_content_instance.replaytoemail]
                email_host = EmailMessage(
                    email_subject_host,
                    email_message_host,
                    email_from_host,
                    email_to_host
                )
                email_host.send()
            
            # Save the subscriber object to the database
            subscriber.save()

            return redirect('blog')

    return redirect('blog')

def download_subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Save the email to the database
            subscriber, created = Subscriber.objects.get_or_create(email=email)

            # Send a confirmation email to the subscriber
            email_subject_subscriber = 'Newsletter Subscription Confirmation'
            email_message_subscriber = 'Dear Subscriber,\nCongratulations! You have successfully subscribed to our newsletter.'
            email_from = f'Axom Lights <{settings.EMAIL_HOST_USER}>'
            email_to_subscriber = [email]
            email_subscriber = EmailMessage(
                email_subject_subscriber,
                email_message_subscriber,
                email_from,
                email_to_subscriber
            )
            email_subscriber.send()

            # Retrieve the replaytoemail value from the GeneralContent instance
            general_content_instance = GeneralContent.objects.first()  # Assuming you retrieve a single instance
            if general_content_instance:
                email_to = [general_content_instance.replaytoemail]

                # Send a notification email to the EMAIL_HOST_USER
                email_subject_host = 'New Newsletter Subscription'
                email_message_host = f'A new subscription has been made. Email: {email}'
                email_from_host = f'Axom Lights <{settings.EMAIL_HOST_USER}>'
                email_to_host = [general_content_instance.replaytoemail]
                email_host = EmailMessage(
                    email_subject_host,
                    email_message_host,
                    email_from_host,
                    email_to_host
                )
                email_host.send()
            
            # Save the subscriber object to the database
            subscriber.save()


            return redirect('download')

    return redirect('download')


def contactus_subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Save the email to the database
            subscriber, created = Subscriber.objects.get_or_create(email=email)

            # Send a confirmation email to the subscriber
            email_subject_subscriber = 'Newsletter Subscription Confirmation'
            email_message_subscriber = 'Dear Subscriber,\nCongratulations! You have successfully subscribed to our newsletter.'
            email_from = f'Axom Lights <{settings.EMAIL_HOST_USER}>'
            email_to_subscriber = [email]
            email_subscriber = EmailMessage(
                email_subject_subscriber,
                email_message_subscriber,
                email_from,
                email_to_subscriber
            )
            email_subscriber.send()

            # Retrieve the replaytoemail value from the GeneralContent instance
            general_content_instance = GeneralContent.objects.first()  # Assuming you retrieve a single instance
            if general_content_instance:
                email_to = [general_content_instance.replaytoemail]

                # Send a notification email to the EMAIL_HOST_USER
                email_subject_host = 'New Newsletter Subscription'
                email_message_host = f'A new subscription has been made. Email: {email}'
                email_from_host = f'Axom Lights <{settings.EMAIL_HOST_USER}>'
                email_to_host = [general_content_instance.replaytoemail]
                email_host = EmailMessage(
                    email_subject_host,
                    email_message_host,
                    email_from_host,
                    email_to_host
                )
                email_host.send()
            

            # Save the subscriber object to the database
            subscriber.save()


            return redirect('contactus')

    return redirect('contactus')

from .models import Dashboard_Subscriber
def dashboard_subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Save the email to the database
            subscriber, created = Dashboard_Subscriber.objects.get_or_create(email=email)

            # Send a confirmation email to the subscriber
            email_subject_subscriber = 'Newsletter Subscription Confirmation'
            email_message_subscriber = 'Dear Subscriber,\nCongratulations! You have successfully subscribed to our newsletter.'
            email_from = f'PocketFriendly <{settings.EMAIL_HOST_USER}>'
            email_to_subscriber = [email]
            email = EmailMessage(
                email_subject_subscriber,
                email_message_subscriber,
                email_from,
                email_to_subscriber
                    )
            email.send()

            # Send a notification email to the EMAIL_HOST_USER
            email_subject_host = 'New Newsletter Subscription'
            email_message_host = f'A new subscription has been made from Axom Lights Dashboard. Email: {email}.'
            email_from_host = settings.EMAIL_HOST_USER
            email_to_host = [settings.EMAIL_HOST_USER]
            email_host = EmailMessage(
                        email_subject_host,
                        email_message_host,
                        email_from_host,
                        email_to_host
                    )
            email_host.send()

            # Save the subscriber object to the database
            subscriber.save()
            messages.success(request,"You have successfully subscribed PocketFriendlyweb's news letter")
            return redirect('dashboard')

    return redirect('dashboard')


def newslettersubscriberslist(request):
    subscribers_list = Subscriber.objects.all()

    # Number of items to display per page
    items_per_page = 30
    paginator = Paginator(subscribers_list, items_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'subscriberslistcontent.html', {'page_obj': page_obj})


def toggle_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_selected = not product.is_selected
    product.save()
    return redirect('product_list')


 