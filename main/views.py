import json
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView
from django.http import HttpResponseRedirect, JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
# Create your views here.

allmovies = Movie.objects.all()

class MovieListView(ListView):
    model = Movie
    template_name = 'home.html'
    paginate_by = 30
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Київський Кінотеатр: Розклад сеансів та квитки онлайн у центрі Києва'
        context["allmovies"] = allmovies
        return context

def contacts(request):
    context = {'title': 'Контакти - Київський Кінотеатр'}
    context["allmovies"] = allmovies
    return render(request, 'contacts.html', context)

def about(request):
    context = {}
    context["title"] = 'Про нас - Київський Кінотеатр: Наша історія та місія'
    context["allmovies"] = allmovies
    return render(request, 'about.html', context)

class MovieDetailView(DetailView):
    model = Movie
    template_name = "movie.html"
    context_object_name = "movie"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f'{Movie.objects.get(pk=self.kwargs["pk"]).title} - Київський Кінотеатр'
        context["allmovies"] = allmovies
        return context
        
def getCurrentSession(request, movie_id, datetime):
    movie = Movie.objects.get(pk=movie_id)
    price = {
        '11:00:00': 140,
        '14:30:00': 160,
        '18:00:00': 200,
        '21:30:00': 180,
    }[datetime.split('_')[1]]
    currentSession = Session.objects.get_or_create(movie=movie,
                                                   datetime=datetime.replace('_', ' '),
                                                   price=price)
    return JsonResponse({ticket.seat: ticket.isbooked for ticket in currentSession[0].tickets.all()})


def buyTickets(request, movie_id, datetime):
    if request.method == 'POST':
        movie = Movie.objects.get(pk=movie_id)
        currentSession = Session.objects.get(movie=movie, datetime=datetime.replace('_', ' '))
        checkedTickets = request.POST.getlist('data[]')
        for ticket in checkedTickets:
            Ticket.objects.filter(session=currentSession, seat=ticket[1:]).update(isbooked=True)
    return JsonResponse({'message': 'done!'})

def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not username or not email or not password1 or not password2:
            messages.error(request, 'Заповніть всі поля')
            return render(request, 'signup.html')
        if password1 != password2:
            messages.error(request, 'Паролі не співпадають')
            return render(request, 'signup.html')
        user = authenticate(username=username, password=password1)
        if user:
            messages.error(request, 'Користувач з таким іменем вже існує')
            return render(request, 'signup.html')
        if User.objects.filter(email=email).first():
            messages.error(request, 'Користувач з такою поштою вже існує')
            return render(request, 'signup.html')
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        login(request, user)
        return redirect('home')
    context = {'title': 'Реєстрація - Київський Кінотеатр'}
    context["allmovies"] = allmovies
    return render(request, 'signup.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next = request.POST.get('next', '/')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
        else:
            messages.error(request, 'Неправильний логін або пароль')
    return HttpResponseRedirect(next)

def user_logout(request):
    if request.method == 'POST':
        next = request.POST.get('next', '/')
        logout(request)
        return HttpResponseRedirect(next)