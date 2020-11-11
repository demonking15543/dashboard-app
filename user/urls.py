from django.urls import path
from .views import SignupView, LoginView, Logout, user_detail_view
urlpatterns = [
   path('signup/', SignupView.as_view(), name='signup'),

   path('login/', LoginView.as_view(), name='login'),
   path('logout/', Logout, name='logout'),
   path('detail/', user_detail_view, name='user-detail'),


    
]
