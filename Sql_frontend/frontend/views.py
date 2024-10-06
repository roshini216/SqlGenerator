from django.shortcuts import render
from datetime import date
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
import random
from django.core.exceptions import MultipleObjectsReturned
from django.http import JsonResponse
from django.http import QueryDict

# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def home(request):
        return render(request, 'frontend/home.html')


def send_otp_email(otp, email):
    subject = "Verify your Email - {}".format(email)
    print(otp)
    message = "Your 4-digit OTP to verify your account is : " + str(otp) + ". Please don't share it with anyone else"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def send_psw_email(otp, email):
    subject = "Reset your Password - {}".format(email)
    print(otp)
    message = "Your 4-digit OTP to reset your password is : " + str(otp) + ". Please don't share it with anyone else"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def Register(request):
    if request.method == "POST":

        fnd1 = User.objects.filter(email=request.POST['email'].lower())
        # fnd2 = Company.objects.filter(email = request.POST['email'].lower())
        if len(fnd1) == 0:
            request.session['username'] = request.POST['username']
            request.session['email'] = request.POST['email'].lower()
            request.session['password'] = request.POST['password']
            # request.session['role'] = request.POST['role']
            cpswd = request.POST['confirmPassword']

            if request.session['password'] == cpswd:
                # if request.session['role'] == 'applicant':

                request.session['password'] = make_password(request.POST['password'])
                request.session['otp'] = random.randint(1000, 9999)
                print(request.session['otp'])
                send_otp_email(request.session['otp'], request.session['email'])
                messages.success(request, "OTP is sent to your email. Please enter it.")
                return redirect("verifyotppage")
            else:
                messages.error(request, "Password and Confirm Password do not match. Please try again")
                return redirect("register")
        else:
            messages.error(request, "User already exists. Please login")
            return redirect("login")
    else:
        return render(request, "frontend/register.html")


def Login(request):
    if request.method == "POST":
        email = request.POST['username'].lower()
        pswd = request.POST['password']
        fnd1 = User.objects.filter(username=request.POST['username'].lower())
        # fnd2 = Company.objects.filter(email = request.POST['email'].lower())
        if len(fnd1) > 0:
            if check_password(pswd, fnd1[0].password):
                request.session['id'] = fnd1[0].id
                request.session['username'] = fnd1[0].username

                return redirect("home")
            else:
                messages.error(request, "Please enter a valid password")
                return redirect("login")

        else:
            messages.error(request, "User does not exist. Please register.")
            return redirect("register")
    else:
        return render(request, "frontend/index.html")


def Logout(request):
    if 'email' in request.session:

        del request.session['id']
        del request.session['username']
        del request.session['email']
        # del request.session['role']
        return redirect("login")
    else:
        return redirect("login")


def VerifyOTPPage(request):
    return render(request, "frontend/otp.html")


def FpEmailPage(request):
    return render(request, "frontend/fp-email.html")


def FpOTPPage(request):
    return render(request, "frontend/otp.html")


def FpPasswordPage(request):
    return render(request, "frontend/forgot_password.html")


def VerifyOTP(request):
    if request.method == "POST":
        username = request.session['username']

        email = request.session['email']
        mainotp = request.POST['otp']
        print(type(mainotp), type(request.session['otp']))
        if request.session['otp'] == int(mainotp):
            applicant = User.objects.create(
                username=username,
                email=email,
                password=request.session['password']
            )
            del request.session['password']
            del request.session['email']
            del request.session['username']

            del request.session['otp']
            messages.success(request, "You have Registered successfully. Login to continue.")
            return redirect("login")
        else:
            messages.error(request, "Invalid OTP. Please try again")
            return redirect("verifyotppage")




def FpEmail(request):
    if request.method == "POST":
        email = request.POST['email'].lower()
        user1 = User.objects.filter(email=email)
        # user2 = Company.objects.filter(email = email)
        if user1:
            request.session['email'] = email
            request.session['role'] = 'applicant'
            request.session['otp'] = random.randint(1000, 9999)
            send_psw_email(request.session['otp'], request.session['email'])
            return redirect("fpotppage")


        else:
            messages.error(request, "User does not exist. Please Register")
            return redirect("register")


def FpOTP(request):
    if request.method == "POST":
        eml = request.session['email'].lower()
        mainotp = request.POST['otp']
        if request.session['otp'] == int(mainotp):
            del request.session['otp']
            return redirect("fppasswordpage")
        else:
            messages.error(request, "Invalid OTP. Please try again")
            return redirect("fpotppage")


def FpPassword(request):
    if request.method == "POST":
        fnd = User.objects.get(email=request.session['email'])
        pswd = request.POST['password']
        cpswd = request.POST['confirmPassword']
        if pswd == cpswd:
            fnd.password = make_password(pswd)
            fnd.save()
            del request.session['email']
            del request.session['role']
            messages.success(request, "Password changed successfully. Login to continue.")
            return redirect("login")
        else:
            messages.error(request, "Password and Confirm Password do not match. Please try again")
            return redirect("fppasswordpage")



