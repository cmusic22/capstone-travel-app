from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm

# Create your views here.

"""If this is a POST request, the user clicked the Add button in the form.
Chick if the new place is valid, if it is, save the new place to the database,
and redirect to this same page.
This creates a GET request to this same route.

If not a POST route, or Place is not valid, display a page with a list of
places and a form to add a new place. """


def place_list(request):

	if request.method == 'POST':
		form = NewPlaceForm(request.POST)
		place = form.save() #create a new Place from the form
		if form.is_valid(): #Checks against DB constraints
			place.save() #saves to the DB
			return redirect('place_list') #redirects to GET view with name place_list, which is this same view

	places = Place.objects.filter(visited=False).order_by('name')
	new_place_form = NewPlaceForm()
	return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})

def places_visited(request):
	visited = Place.objects.filter(visited=True)
	return render(request, 'travel_wishlist/visited.html', {'visited': visited})

def place_was_visited(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        place = get_object_or_404(Place, pk=pk)
        place.visited = True
        place.save()
    
    return redirect('place_list')