from django.test import TestCase
from django.urls import reverse

from .models import Place

class TestHomePageIsEmptyList(TestCase):

	def test_load_home_shows_empty_list(self):
		response = self.client.get(reverse('place_list'))
		self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
		self.assertFalse(response.context['places'])
		self.assertContains(response, 'You have no places in your wishlist')

class TestWishList(TestCase):
	fixtures = ['test_places']

	def test_view_wishlist_contains_not_visited_places(self):
		response = self.client.get(reverse('place_list'))
		self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

		self.assertContains(response, 'Tokyo')
		self.assertContains(response, 'New York')
		self.assertNotContains(response, 'San Francisco')
		self.assertNotContains(response, 'Moab')

class TestNoVisitors(TestCase):
	fixtures = ['test_not_visited']

	def test_wishtlist_no_visits(self):
		response = self.client.get(reverse('places_visited'))
		self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
		self.assertMultiLineEqual('You have not visited any places yet.', 'You have not visited any places yet.', msg=None) #found on https://docs.python.org/3/library/unittest.html

class TestVisitedList(TestCase):
	fixtures = ['test_places']

	def test_visited_list(self):
		response = self.client.get(reverse('places_visited'))
		self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
		self.assertListEqual('', '') #found on https://docs.python.org/3/library/unittest.html

class TestAddNewPlace(TestCase):

	def test_add_new_unvisited_place_to_wishlist(self):

		response = self.client.post(reverse('place_list'), {'name': 'Tokyo', 'visited': False}, follow=True)

		#Check correct template was used
		self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

		#what data was used to populate the template
		response_places = response.context['places']

		#Should be 1 item
		self.assertEqual(len(response_places), 1)
		tokyo_response = response_places[0]

		#Expect this data to be in the database. Use get() to get data with
		#the values expected. Will throw an exception if no data, or more tan
		#own row, matches. Remember throwing an exception will cause this test to fail
		tokyo_in_database = Place.objects.get(name='Tokyo', visited=False)

		# Is the data used to render the template, the same as the data in the database?
		self.assertEqual(tokyo_response, tokyo_in_database)
