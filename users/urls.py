from django.urls import path
from .views import SignupView, CustomLoginView,CustomPasswordChangeView, HomeView,ListProfileView,UpdateProfileView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password/change/', CustomPasswordChangeView.as_view(), name='changepassword'),
    path('', HomeView.as_view(), name='home'),
    path('profile/', ListProfileView.as_view(), name='list_profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
]
 