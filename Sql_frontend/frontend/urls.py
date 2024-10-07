from django.urls import path
from .views import *
urlpatterns = [
    path('', Login,name="login"),
    path('register/',Register,name="register"),
    path('forgot_password/',FpEmail,name="forgot_password"),
    path('home/', home,name="home"),
    path("logout/", Logout, name="logout"),

    path("otp-verification/", VerifyOTPPage, name="verifyotppage"),
    path("forgot-password-email/", FpEmailPage, name="fpemailpage"),
    path("forgot-password-otp/", FpOTPPage, name="fpotppage"),
    path("reset_password/", FpPasswordPage, name="fppasswordpage"),
    path("verify-otp/", VerifyOTP, name="verify-otp"),
    path("fp-email/", FpEmail, name="fp-email"),
    path("fp-otp/", FpOTP, name="fp-otp"),
    path("fp-password/", FpPassword, name="fp-password"),


]

