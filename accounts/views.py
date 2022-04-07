from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
from .models import Admin, Book


def home(request):
    if request.method == 'POST':
        signout = request.POST.get('logout')
        if signout:
            logout(request)
            return redirect('/login')
    else:
        books = Book.objects.all()
        context = {'books': books }
        return render(request,'home.html',context)

def signup(request):
    if request.method == 'POST':
        context = { }
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            context['error'] = "Password and Repeat password doesn't match"
            return render(request,'signup.html',context)
        else:
            with transaction.atomic():
                user = User.objects.filter(email = email)
                if len(user) > 0:
                    context['error'] = "Email already exists"
                    return render(request,'signup.html',context)
                else:
                    user = User.objects.create_user(username=email,email=email,password=password)
                    admin = Admin.objects.create(name = name, user = user)
                    return redirect('/login')
    else:
        return render(request,'signup.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,username = email, password = password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            context = { }
            context['error'] = 'Login failed'
            return render(request,'login.html',context)
    return render(request,'login.html')

def add_book(request):
   if request.method == 'POST':
       try:
           with transaction.atomic():
               book_name = request.POST.get('bookName')
               author = request.POST.get('authorName')
               isbn = request.POST.get('isbn')
               publication = request.POST.get('publication')
               if len(book_name) > 0 and len(author) > 0 and len(isbn) > 0 and len(publication) > 0:
                   admin = Admin.objects.filter(user = request.user)
                   if len(admin)>0:
                       book = Book.objects.create(name=book_name,author=author,isbn=isbn,publication=publication)
                   return redirect('/')
               else:
                   return redirect('/')

       except Exception as e:
           return redirect('/')


def update_book(request):
  if request.method == "POST":
      try:
          with transaction.atomic():
              uid = request.POST.get('uid')
              book_name = request.POST.get('bookName')
              author = request.POST.get('authorName')
              isbn = request.POST.get('isbn')
              publication = request.POST.get('publication')
              if len(book_name) > 0 and len(author) > 0 and len(isbn) > 0 and len(publication) > 0:
                  admin = Admin.objects.filter(user=request.user)
                  if len(admin) > 0:
                      books = Book.objects.filter(uid = uid)
                      if len(books) > 0:
                          book =books[0]
                          book.name = book_name
                          book.author = author
                          book.isbn = isbn
                          book.publication = publication
                          book.save()
                      return redirect('/')
              else:
                  return redirect('/')
      except Exception as e:
          return redirect('/')

def delete_book(request):
  if request.method == "POST":
      try:
          with transaction.atomic():
              uid = request.POST.get('uid')
              admin = Admin.objects.filter(user=request.user)
              if len(admin) > 0:
                  books = Book.objects.filter(uid = uid)
                  if len(books) > 0:
                      book =books[0]
                      book.delete()
                  return redirect('/')
      except Exception as e:
          return redirect('/')

