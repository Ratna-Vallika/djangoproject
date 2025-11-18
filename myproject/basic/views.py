from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
import json
from django.views.decorators.csrf import csrf_exempt
from basic.models import Student

# Create your views here.
def sample(request):
    return HttpResponse('hello world ')

def sample1(request):
    return HttpResponse('welcome to django!!! ')

def sampleInfo(request):
    #data={"name":"vallika","age":21,"city":"hyd"}
    #return JsonResponse(data)
    #data=[4,5,6,9]
    data={'result':[4,5,6,9]}
    return JsonResponse(data,safe=False)

def dynamicResponse(request):
    name=request.GET.get("name",'')
    city=request.GET.get("city",'hyd') 
    return HttpResponse(f"hello {name} from {city}")
#calculator
def calculator(request):
    a=request.GET.get("a")
    b=request.GET.get("b") 
    operation=request.GET.get("operation",'').lower()

    if a is None or b is None:
        return JsonResponse({'please provide both a and b in query values'},status=400)
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        return JsonResponse({'error': 'Invalid input. a and b must be numbers.'}, status=400)
    
    if operation=='add':
       result=a+b
    elif operation == 'subtract':
        result = a - b
    elif operation == 'multiply':
        result = a * b
    elif operation == 'divide':
        if b == 0:
            return JsonResponse({'error': 'Division by zero is not allowed.'}, status=400)
        result = a / b
    else:
        return JsonResponse({'error': 'Invalid operation. Use add, subtract, multiply, or divide.'}, status=400)
    
    return JsonResponse({
        'a':a,
        "b":b,
        'operation':operation,
        'result':result
    })

#to test database connection
def health(request):
    try:
        with connection.cursor() as c:
            c.execute("SELECT 1")
        return JsonResponse({"status":"ok","db":"connected"})
    except Exception as e:
        return JsonResponse({"status":"error","db":str(e)})

@csrf_exempt          
def addStudent(request):
    print(request.method)
    if request.method =='POST':
        data=json.loads(request.body)
        student=Student.objects.create(
            name=data.get('name'),
            age=data.get('age'),
            email=data.get('email')
            )
        return JsonResponse({"status":"success","id":student.id},status=200) 
    
    elif request.method=="GET":
        result=list(Student.objects.values())
        print(result)
        return JsonResponse({"status":"ok","data":result},status=200) 
    
    elif request.method=="PUT":
        data=json.loads(request.body)
        ref_id=data.get("id")#getting id
        new_email=data.get("email") #getting email
        existing_student=Student.objects.get(id=ref_id)#fetched the object as per table
        #print(existing_student)
        existing_student.email=new_email#updating new email
        existing_student.save()
        upadted_data=Student.objects.filter(id=ref_id).values().first()
        return JsonResponse({"status":"data updated successfully","updated_data":upadted_data},status=200)
     
    elif request.method=="DELETE":
        data=json.loads(request.body)
        ref_id=data.get("id")
        get_deleting_data=Student.objects.filter(id=ref_id).values().first()
        to_be_delete=Student.objects.get(id=ref_id)
        to_be_delete.delete()
        return JsonResponse({"status":" success","message":"student record deleted successfully","deleted_data":get_deleting_data},status=200) 
    return JsonResponse({"error":"use post method"},status=400)

def job1 (request):
    return JsonResponse({"message":"u have successfully applied for job1"},status=200)
def job2(request):
    return JsonResponse({"message":"u have successfully applied for job2"},status=200)
     

