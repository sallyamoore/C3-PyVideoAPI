from django.conf.urls import patterns, url

urlpatterns = patterns(
    'api.views',
    url(r'^customers/$', 'customer_list', name='customer_list'),
    url(r'^customers/name/$', 'customers_by_name', name='customers_by_name'),
    url(r'^customers/registered_at/$', 'customers_by_registered_at', name='customers_by_registered_at'),
    url(r'^movies/$', 'movie_list', name='movie_list'),
    url(r'^rentals/$', 'rental_list', name='rental_list'),

)