from django.urls import path

from stations.views import NewStationListView

urlpatterns = [
    path('/update', NewStationListView.as_view()),
]