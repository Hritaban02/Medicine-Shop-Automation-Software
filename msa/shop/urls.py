from django.urls import path
from . import views, sell, supply


urlpatterns = [

    # Abhishek
    path('', views.home, name='home'),
    path('login', views.loginpage, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('newsupply', supply.newsupply, name='newsupply'),
    path('newsupplymed/<str:id>', supply.newsupplymed, name='newsupplymed'),
    path('sellmedicine', sell.sellmedicine, name='sellmedicine'),
    path('printreceipt/<str:trans>', sell.printreceipt,   name='printreceipt'),
    path('printvendorreceipt/<str:trans>',
         supply.printvendorreceipt, name='printvendorreceipt'),
    path('change_password', views.change_password, name='change_password'),



    # Hritaban
    path('search', views.search, name='search'),
    path('newmed', views.newmed, name='newmed'),
    path('below_threshold', views.below_threshold, name='below_threshold'),
    path('listOfMed', views.listOfMed, name='listOfMed'),
    

    # Saumyak
    path('expired', views.expired, name='expired'),
    path('usable', views.usable, name='usable'),
    path('addvendor', views.addvendor, name='addvendor'),
    path('threshold', views.threshold, name='threshold'),
    path('revenue', views.revenue, name='revenue'),
    path('revenue_data', views.calc, name='revenue_data'),
    path('clear_exp', views.clear_exp, name='clear_exp')
]
