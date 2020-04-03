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

class TestVisitedList(TestCase)		