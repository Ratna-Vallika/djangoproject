from django.http import JsonResponse
import re,json
from basic.models import Users

class basicMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        print(request,'hello')
        if(request.path=="/student/"):
            print(request.method,'method')
            print(request.path)
        response=self.get_response(request)
        return response
'''import json   
class signupMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self, request):
        data=json.loads(request.body)
        username=data.get("username")
        email=data.get("email")
        dob=data.get("dob")
        password=data.get("pswd")
        #check username,email,dob,password rules with regex'''
  
class sscMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self, request):
        if(request.path in ["/job1/","/job2/"]):
            ssc_result=request.GET.get("ssc")
            print(ssc_result)
            if(ssc_result !='True'):
                return JsonResponse({"error":"u should qualify atleast ssc for applying this job"},status=400)
        return self.get_response(request)
    
class medicalFitMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self, request):
        if request.path =="/job1/":
            medical_fit_result=request.GET.get("medically_fit")
            if (medical_fit_result !='True'):
                return JsonResponse({"error":"u qare not medically fit this job role"},status=400)
        return self.get_response(request)

class AgeMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self, request):
        if(request.path in ["/job1/","/job2/"]):
            Age_checker=int(request.GET.get("age",17))
            if (Age_checker >25 and Age_checker <18):
                return JsonResponse({"error":"age must be in between 18 and 25"},status=400)
        return self.get_response(request)
    

class UsernameMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self, request):
        if (request.path =="/signUp/"):
            data=json.loads(request.body)
            Username=data.get("username"," ")
            #checks username is empty or not
            if not Username:
                return JsonResponse({"error":"username is required"},status=400)
            #checks character length of username
            if (len(Username)< 3 or len(Username)> 20):
                return JsonResponse({"error":"username should contains  3 to 20 characters"},status=400)
            #checking starting and ending of username
            if Username[0] in "._" or Username[-1] in "._":
                return JsonResponse({"error":"username should not starts or end with . or _"},status=400)
            #checks allowed characters
            if not re.match(r"^[a-zA-Z0-9._]+$",Username):
                return JsonResponse({"error":"username should contains letters,numbers,dot,underscore"},status=400)
            #checks .. and __
            if ".." in Username or "__" in Username:
                return JsonResponse({"error:cannot have .. or __"},status=400)
        return self.get_response(request)

#email should not be empty  ,basic email pattern ,if duplicate email found --show email alraedy exists  
class EmailMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self, request):
        if (request.path =="/signUp/"):
            data=json.loads(request.body)
            email=data.get("email","")
            #email should not be empty
            if not email:
                 return JsonResponse({"error": "email is required"}, status=400)
            #basic eamil pattern
            email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(email_pattern,email):
                return JsonResponse({"error": "invalid email format"}, status=400)
            #duplicate email check
            if Users.objects.filter(email=email).exists():
                return JsonResponse({"error": "email already exists"}, status=400)
        return self.get_response(request)
                  
#normal password pattern for strong password
class PasswordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if (request.path == "/signUp/"):
            try:
                data = json.loads(request.body)
            except:
                data = {}
            password = data.get("password", "")
            # 1) Password should not be empty
            if not password:
                return JsonResponse({"error": "password is required"}, status=400)
            # 2) Check length
            if len(password) < 8 or len(password) > 20:
                return JsonResponse({"error": "password must be 8-20 characters long"}, status=400)
            # 3) Check for at least one lowercase, one uppercase, one digit, one special character
            pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,20}$'
            if not re.match(pattern, password):
                return JsonResponse({"error": "password must contain at least one uppercase, lowercase, digit, and special character (@#$%^&+=!)"}, status=400)
        return self.get_response(request)
            
            
    