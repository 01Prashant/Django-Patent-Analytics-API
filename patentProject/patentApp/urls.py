from django.urls import path
from . import views

urlpatterns = [
    path('summary/', views.patent_summary),
    path('query/', views.query_patents),
]