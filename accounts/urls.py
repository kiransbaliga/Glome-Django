from django.urls import path

from  .views import create_user_view, login_view, ProfileView, OtpView, RetryOtpView, UsernameView

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', create_user_view, name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('account/verify', OtpView.as_view(), name='otp-view'),
    path('account/verify/retry', RetryOtpView.as_view(), name='retry-otp-view'),
    path('account/set-username', UsernameView.as_view(), name='username-view'),
]


#8481