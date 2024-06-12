from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 

urlpatterns=[
 
   
    path('map_view/', views.map_view, name='map_view'),
    path('',views.index, name='index'),

    path('aboutus/', views.aboutus, name='aboutus'),
    path('Product/',views.product, name="product"),
    path('Blog/',views.blog, name="blog"),
    path('Contact/',views.contact, name="contact"),
    path('Sustainability/',views.sustainability, name="sustainability"),
    path('Download/',views.download, name="download"),
    path('Product_Detail/',views.productdetail, name="productdetail"),
    path('Blog/<slug:slug>/', views.blogdetail, name='blogdetail'),
    path('login/', views.login_form, name='login'),
    path('accounts/login/', views.login_form, name='login_form'),
   
    path('register/',views.register_form,name="register"),
    path('logout/', views.logout, name='logout'),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('category/toggle/<int:category_id>/', views.toggle_category, name='toggle_category'),
    path('product/toggle/<int:product_id>/', views.toggle_product, name='toggle_product'),
    path('subscribe_newsletter',views.subscribe_newsletter,name="subscribe_newsletter"),
    path('about_subscribe_newsletter',views.about_subscribe_newsletter,name="about_subscribe_newsletter"),
    path('product_subscribe_newsletter',views.product_subscribe_newsletter,name="product_subscribe_newsletter"),
    path('blog_subscribe_newsletter',views.blog_subscribe_newsletter,name="blog_subscribe_newsletter"),
    path('download_subscribe_newsletter',views.download_subscribe_newsletter,name="download_subscribe_newsletter"),
    path('contactus_subscribe_newsletter',views.contactus_subscribe_newsletter,name="contactus_subscribe_newsletter"),
    path('dashboard_subscribe_newsletter',views.dashboard_subscribe_newsletter,name="dashboard_subscribe_newsletter"),
    path('newslettersubscriberslist',views.newslettersubscriberslist,name="newslettersubscriberslist"),
    path('map_input/', views.map_input, name='map_input'),
#generalcontents urls

    path('generalcontent/', views.generalcontent, name='generalcontent'),
    
    path('site_primary_info/', views.site_primary_info, name='site_primary_info'),
    path('site_address_info/', views.site_address_info, name='site_address_info'),

    path('site_logo_favicon/', views.site_logo_favicon, name='site_logo_favicon'),
    path('contact_emails/', views.contact_emails, name='contact_emails'),

    path('update_contact_numbers/', views.update_contact_numbers, name='update_contact_numbers'),
    path('update_social_media_links/', views.update_social_media_links, name='update_social_media_links'),

    path('update_seotags/', views.update_seotags, name='update_seotags'),
    path('update_google_analytics/', views.update_google_analytics, name='update_google_analytics'),

    path('update_style/', views.update_style, name='update_style'),


    # pagecontent
    path('pagecontent/', views.pagecontent, name='pagecontent'),
    path('create_carousal/', views.create_carousal, name='create_carousal'),
    path('carousal_list_table/',views.carousal_list_table,name="carousal_list_table"),
    path('carousal/delete/<slug:slug>/', views.delete_carousal, name='delete_carousal'),
    path('homepage/', views.homepage, name='homepage'),
    path('About_Us/', views.About_Us, name='About_Us'),
    path('blog_Page/', views.blog_Page, name='blog_Page'),
    path('Download_Page/', views.Download_Page, name='Download_Page'),
    path('update_sustainability_content/', views.update_sustainability_content, name='update_sustainability_content'),


    path('sub_category/', views.sub_category, name='sub_category'),
    path('subcategory_list_table/',views.subcategory_list_table,name="subcategory_list_table"),
    path('update_sub_category/<slug:slug>/', views.update_sub_category, name='update_sub_category'),
    path('subcategory/delete/<slug:slug>/', views.delete_subcategory, name='delete_subcategory'),

    path('product_category/', views.product_category, name='product_category'),
    path('update_category/<slug:slug>/', views.update_category, name='update_category'),

    path('category_list_table/',views.category_list_table,name="category_list_table"),
    path('category/delete/<slug:slug>/', views.delete_category, name='delete_category'),
    path('product_page/', views.product_page, name='product_page'),
    path('product-list/', views.product_list, name='product_list'),
    path('product/delete/<slug:slug>/', views.delete_product, name='delete_product'),
    path('update_product/<slug:slug>/', views.update_product, name='update_product'),
    path('addblog/', views.addblog, name='addblog'),
    path('blog-list/', views.blog_list, name='blog_list'),
    path('blog/delete/<slug:slug>/', views.delete_blog, name='delete_blog'),
    path('update_blog/<slug:slug>/', views.update_blog, name='update_blog'),
    path('Contact us/', views.contactus, name='contactus'),
    path('contact_us_list/', views.contact_us_list, name='contact_us_list'),
    path('Product Details/<slug:slug>/', views.productdetail, name='productdetail'),
    path('Product/<slug:slug>/', views.subcategory_details, name='subcategory_details'),
    path('carousal/update/<slug:slug>/', views.update_carousal, name='update_carousal'),

   
    
    #reset password 

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/passwordresetform.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/passwordresetdone.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(template_name='registration/passwordresetconfirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/passwordresetcomplete.html'), name='password_reset_complete'),

    ]