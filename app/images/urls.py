from django.urls import path
from images import views

app_name = "images"

urlpatterns = [
  path('upload/', views.ImageCreateView.as_view({'post': 'create'}), name='upload'),
  path('getall/', views.ImageListView.as_view({'get': 'list'}), name='getall'),
]