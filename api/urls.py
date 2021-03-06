from django.conf.urls import patterns, url

urlpatterns = patterns(
    'api.views',
    url(r'^customers/$', 'customer_list', name='customer_list'),
    url(r'^customers/(?P<column>.+)/$', 'customers_by_column', name='customers_by_column'),

    url(r'^movies/$', 'movie_list', name='movie_list'),
    url(r'^movies/(?P<column>.+)/$', 'movies_by_column', name='movies_by_column'),
    url(r'^movie/(?P<title>.+)/$', 'movie', name='movie'),

    url(r'^rentals/$', 'rental_list', name='rental_list'),
    url(r'^rentals/checkout/$', 'checkout_checkin', name='checkout_checkin'),
    url(r'^rentals/checkin/(?P<movie_title>.+)/(?P<customer_pk>.+)/$', 'checkout_checkin', name='checkout_checkin')
)
