from . import views
from django.urls import path
from django.contrib.auth import views as auth_view
from .forms import LoginForm,MyPasswordResetForm,MyPasswordChangeForm,MySetPasswordForm
urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('category/<str:val>',views.CategoryView.as_view(), name='category'),
    path('category-title/<str:val>',views.CategoryTitle.as_view(), name='category-title'),
    path('product/<int:pk>',views.productDetail.as_view(),name="product" ),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('address/',views.address,name='address'),
    path('updateAddress/<int:pk>',views.updatAddress.as_view(),name='updateAddress'),
    
    #add to cart
    path('add-to-cart/',views.add_to_cart, name='add_to_cart'),
    path('cart/',views.show_cart,name='showcart' ),
    path('checkout/', views.checkout.as_view(),name='checkout'),

    path("pluscart/",views.plus_cart),
    path("minuscart/",views.minus_cart),
    path('removecart/',views.remove_cart),
    #login authentication 
    path('register/',views.CustomerRegistrationView.as_view(), name='register'),
    path('accounts/login/',auth_view.LoginView.as_view(template_name ='website/login.html',authentication_form = LoginForm),name='login'),
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='website/changepassword.html', form_class = MyPasswordChangeForm,success_url = '/passwordchangedone'), name='passwordchange' ),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='website/changepassworddone.html'), name='passwordchangedone' ),
    path('logout/',auth_view.LogoutView.as_view(next_page = 'login'), name='logout'),
    
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name ='website/password_reset.html',form_class = MyPasswordResetForm),name="password_reset"),
    path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name ='website/password_reset_done.html'),name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name ='website/password_reset_confirm.html',form_class = MySetPasswordForm),name="password_reset_confirm"),
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name ='website/password_reset_conplete.html',),name="password_reset_complete"),
]
