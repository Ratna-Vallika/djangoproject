from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

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


    

