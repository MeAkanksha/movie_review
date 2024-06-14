from django.urls import path
from movie import views


urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('details/<int:id>/', views.details, name='details'),
    path('add/', views.add_movies, name='add'),
    path('edit/<int:id>/', views.edit_movies, name='edit'),
    path('delete/<int:id>/', views.delete_movies, name='delete'),
    path('addreview/<int:id>/', views.add_review, name='add_review'),
    path('editreview/<int:movie_id>/<int:review_id>/', views.edit_review, name='edit_review'),
    path('deletereview/<int:movie_id>/<int:review_id>/', views.delete_review, name='delete_review'),
]
