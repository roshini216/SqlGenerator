
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
import random
from django.core.exceptions import ValidationError
from .forms import UploadFileForm
import openpyxl
import csv





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



def handle_uploaded_csv(f):
    # Check file size (limit to 5MB)
    if f.size > 5 * 1024 * 1024:
        raise ValidationError("File size should be under 5MB")
    print(f"Uploading file: {f.name}")
    # Check file format
    if not f.name.endswith('.csv'):
        raise ValidationError("Unsupported file format. Please upload a CSV file.")

    # Handle CSV file
    try:
        reader = csv.reader(f.read().decode('utf-8').splitlines())
        for row in reader:
            # Process each row
            # print(row)
            print(f"Processing row: {row}")
            print("CSV file processed successfully")
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        raise ValidationError("Corrupted CSV file")

def handle_uploaded_excel(f):
    # Check file size (limit to 5MB)
    print(f"Uploading file: {f.name}")
    if f.size > 5 * 1024 * 1024:
        raise ValidationError("File size should be under 5MB")
    print("File size is within the limit")
    # Check file format
    if not (f.name.endswith('.xlsx') or f.name.endswith('.xls')):
        raise ValidationError("Unsupported file format. Please upload an Excel file.")
    print("File format is Excel")
    # Handle Excel file
    try:
        wb = openpyxl.load_workbook(f)
        sheet = wb.active
        for row in sheet.iter_rows(values_only=True):
            # Process each row
            # print(row)
            print(f"Processing row: {row}")
            print("Excel file processed successfully")
    except Exception as e:
        print(f"Error processing Excel file: {e}")
        raise ValidationError("Corrupted Excel file")


def upload_csv(request):
    if request.method == 'POST':
        print("Received POST request for CSV upload")
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                handle_uploaded_csv(request.FILES['csvfile'])
                print("CSV file uploaded successfully")
                messages.success(request, 'CSV file uploaded successfully!')
            except ValidationError as e:
                form.add_error('csvfile', e)
                print(f"Validation error: {e}")
                messages.error(request, str(e))
        else:
            print("Form is not valid")
            messages.error(request, 'Invalid form submission.')
    else:
        form = UploadFileForm()
        print("Rendering upload form for CSV")

    return render(request, 'upload.html', {'form': form})


def upload_excel(request):
    if request.method == 'POST':
        print("Received POST request for Excel upload")
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")
            try:
                handle_uploaded_excel(request.FILES['excelfile'])
                print("Excel file uploaded successfully")
                messages.success(request, 'Excel file uploaded successfully!')
            except ValidationError as e:
                form.add_error('excelfile', e)
                print(f"Validation error: {e}")
                messages.error(request, str(e))
        else:
            print("Form is not valid")
            messages.error(request, 'Invalid form submission.')
    else:
        form = UploadFileForm()
        print("Rendering upload form for Excel")

    return render(request, 'upload.html', {'form': form})