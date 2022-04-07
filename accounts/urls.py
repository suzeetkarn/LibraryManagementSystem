
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.home),
    path('login',views.login_view),
    path('signup',views.signup),
    path('add-book',views.add_book),
    path('update-book',views.update_book),
    path('delete-book',views.delete_book),

]
