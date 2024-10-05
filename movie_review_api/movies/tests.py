from django.test import TestCase
from django.urls import reverse

class MovieSearchTest(TestCase):
    def test_valid_movie_search(self):
        response = self.client.post(reverse('movies:home'), {'movie_title': 'Inception'})
        self.assertEqual(response.status_code, 200)  # Check if the response is OK
        self.assertContains(response, 'Inception')   # Check if the result contains the movie title

class MovieDetailTest(TestCase):
    def test_movie_detail_view(self):
        movie_title = 'Inception'
        response = self.client.get(reverse('movies:movie_detail', kwargs={'movie_title': movie_title}))
        self.assertEqual(response.status_code, 200)  # Check if the response is OK
        self.assertContains(response, 'Inception')  # Ensure the movie detail page contains the correct movie

