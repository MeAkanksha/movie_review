from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.db.models import Avg

# Create your views here.
def home(request):
    query = request.GET.get("title")
    allMovies = None
    
    if query:
        allMovies = Movie.objects.filter(name__icontains=query)
    else:
        allMovies = Movie.objects.all()

    print(allMovies)
    context = {
        'movies' : allMovies
    }
    return render(request, 'index.html', context)

# default page
def details(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=id).order_by("-comment")

    average = reviews.aggregate(Avg("rating"))["rating__avg"]
    if average == None:
        average = 0
    average = round(average,2)
    context = {
        'movie':movie,
        'reviews':reviews,
        'average':average
    }
    return render(request, 'details.html', context)


# add movies to the database
def add_movies(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == "POST":
                form = MovieForm(request.POST or None)

                #create if the form is valid
                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect("home")

            else:
                form = MovieForm()
            return render(request, 'addmovies.html', {'form':form, "controller":'Add Movie'})

        # if they are not admin
        else:
            return redirect('home')
    # if they are not logged in
    return redirect('accounts:login')


# Edit the movie
def edit_movies(request,id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # get the movie linked with id
            movie = Movie.objects.get(id=id)

            # form check
            if request.method == 'POST':
                form = MovieForm(request.POST or None, instance=movie)
                # check if form is valid
                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect('details', id)
            
            else:
                form = MovieForm(instance=movie)
            return render(request, 'addmovies.html', {'form':form, "controller":'Edit Movie'})

        # if they are not admin
        else:
            return redirect('home')
    # if they are not logged in
    return redirect('accounts:login')


# delete the movie
def delete_movies(request,id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # get the movies
            movie = Movie.objects.get(id=id)

            #delete the movie
            movie.delete()
            return redirect('home')

        # if they are not admin
        else:
            return redirect('home')
    # if they are not logged in
    return redirect('accounts:login')


# for add review
def add_review(request, id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id=id)
        if request.method == 'POST':
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)
                data.comment = request.POST['comment']
                data.rating = request.POST['rating']
                data.user = request.user
                data.movie = movie
                data.save()
                return redirect('details', id)
        
        else:
            form = ReviewForm()
        return render(request, 'details.html', {'form':form})
    else:
        return redirect('accounts:login')


# for edit review
def edit_review(request, movie_id, review_id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id=movie_id)
        review = Review.objects.get(movie=movie, id=review_id)


        #check if the review was done by the logged in user
        if request.user == review.user:
            # grant permission
            if request.method == 'POST':
                form = ReviewForm(request.POST, instance=review)
                if form.is_valid():
                    data = form.save(commit=False)
                    if (data.rating >10) or (data.rating <0):
                        error = "Out of range. Please select rating from 0 to 10."
                        return render(request, 'editreview.html', {'error':error, 'form':form})
                    else:
                        data.save()
                        return redirect('details', movie_id)
            
            else:
                form = ReviewForm(instance=review)
            return render(request, 'editreview.html', {'form':form})
        else:
            return redirect('details', movie_id)
    else:
        return redirect('accounts:login')


# delete review
def delete_review(request, movie_id, review_id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id=movie_id)

        #review
        review = Review.objects.get(movie=movie, id=review_id)


        #check if the review was done by the logged in user
        if request.user == review.user:
            # grant permission to delete
            review.delete()
    
        return redirect('details', movie_id)

    else:
        return redirect('accounts:login')





