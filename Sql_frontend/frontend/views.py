
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
import random





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
        email = request.POST['email'].lower()
        fnd1 = User.objects.filter(email=email)

        if fnd1.exists():  # User already exists
            messages.error(request, "User already exists. Please login.")
            return redirect("register")  # Redirect to login page

        username = request.POST['username']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']

        if password != confirmPassword:
            messages.error(request, "Password and Confirm Password do not match. Please try again.")
            return redirect("register")  # Redirect back to registration page



        request.session['username'] = username
        request.session['email'] = email
        request.session['password'] = make_password(password)  # Store hashed password in session
        request.session['otp'] = random.randint(1000, 9999)

        # Send OTP email for verification
        send_otp_email(request.session['otp'], email)
        messages.success(request, "OTP is sent to your email. Please enter it.")
        return redirect("verifyotppage")
    else:
        return render(request, "frontend/register.html")

def Login(request):
    if request.method == "POST":
        username = request.POST['username'].lower()
        pswd = request.POST['password']
        user = User.objects.filter(username=username).first()



        if user:
            if check_password(pswd, user.password):
                request.session['id'] = user.id
                request.session['username'] = user.username
                return redirect("home")
            else:
                messages.error(request, "Invalid password. Please try again.")
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

        return redirect("login")
    else:
        return redirect("login")


def VerifyOTPPage(request):
    return render(request, "frontend/otp.html")


def FpEmailPage(request):
    return render(request, "frontend/forgot_password.html")


def FpOTPPage(request):
    return render(request, "frontend/reset_password_otp.html")


def FpPasswordPage(request):
    return render(request, "frontend/reset_password.html")


def VerifyOTP(request):
    if request.method == "POST":

        username = request.session['username']

        email = request.session['email']
        mainotp = request.POST['otp']
        print(f"Received OTP: {mainotp}, Session OTP: {request.session['otp']}")
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
        print(f"Received email: {email}")  # Debugging line
        user1 = User.objects.filter(email=email)

        if user1:
            request.session['email'] = email
            request.session['otp'] = random.randint(1000, 9999)
            print(f"Generated OTP: {request.session['otp']}")  # Debugging line
            send_psw_email(request.session['otp'], request.session['email'])
            return redirect("fpotppage")
        else:
            messages.error(request, "User does not exist. Please Register")
            return redirect("register")
    else:
        return render(request, "frontend/forgot_password.html")

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
        cpswd = request.POST['Confirmpassword']
        if pswd == cpswd:
            fnd.password = make_password(pswd)
            fnd.save()
            del request.session['email']

            messages.success(request, "Password changed successfully. Login to continue.")
            return redirect("login")
        else:
            messages.error(request, "Password and Confirm Password do not match. Please try again")
            return redirect("fppasswordpage")



