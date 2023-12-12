from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=100, verbose_name='Назва')
    year = models.IntegerField(verbose_name='Рік')
    duration = models.IntegerField(verbose_name='Тривалість', default=0)
    genres = models.CharField(max_length=100, verbose_name='Жанри')
    directors = models.CharField(max_length=100, verbose_name='Режисери')
    image = models.CharField(max_length=300, verbose_name='Посилання на зображення')
    imdb_rating = models.FloatField(verbose_name='Рейтинг')
    description = models.TextField(verbose_name='Опис', default='Опис відсутній', null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    
class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фільм', related_name='sessions')
    datetime = models.DateTimeField(auto_now=False, auto_now_add=False)
    price = models.FloatField(verbose_name='Ціна')
    
    def __str__(self):
        return f'{self.movie.title} - {self.datetime}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for seat in range(90):
            Ticket.objects.get_or_create(session=self, seat=seat)


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Користувач', related_name='tickets', null=True, blank=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name='Сеанс', related_name='tickets')
    seat = models.IntegerField(verbose_name='Місце')
    isbooked = models.BooleanField(verbose_name='Заброньовано', default=False)
    
    def __str__(self):
        return f'{self.session} місце №{self.seat}'