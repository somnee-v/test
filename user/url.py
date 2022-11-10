from django.urls import path, include
from user import views


urlpatterns = [
    path('signup/', views.UserView.as_view(), name='user_view'),
]
