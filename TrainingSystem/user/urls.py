from django.conf.urls import url
from django.urls import path
from . import views
from .views import OtherProfile, AprrovedTrainer, Search

urlpatterns = [
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('<int:pk>/', OtherProfile.as_view(), name='view-profile'),
    path('trainer/<int:pk>/', AprrovedTrainer.as_view(), name='add-trainer'),
    path('search/', Search.as_view(), name='search'),
    path('ajax_calls/search/', views.autocompleteModel, name='auto_search'),

]
