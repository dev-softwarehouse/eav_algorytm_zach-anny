from django.urls import path,include
from .views import fileInputView


urlpatterns = [
    path('data/', fileInputView.as_view(),name='FileInputView')
]