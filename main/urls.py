from django.urls import path
from .views import *

urlpatterns = [
    path('', MovieListView.as_view(), name='home'),
    path('about/', about, name='about'),
    path('contacts/', contacts, name='contacts'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie'),
    path('getCurrentSession/<int:movie_id>/<str:datetime>/', getCurrentSession, name='getCurrentSession'),
    path('buyTickets/<int:movie_id>/<str:datetime>/', buyTickets, name='buyTickets'),
    path('signup/', user_signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
