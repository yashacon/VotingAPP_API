from django.contrib import messages,auth
from django.shortcuts import get_object_or_404
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser,MultiPartParser,FormParser,FileUploadParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status,viewsets
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from .models import *
from .serializers import *
import json
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import parser_classes

@csrf_exempt
def login(request):
    
    if request.method=='POST':
        if request.user.is_authenticated:
            return JsonResponse({'message': "Already logged in!"},status=400)
        data=JSONParser().parse(request)
        try:
            acc=User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return JsonResponse({'message': "Username Not found"},status=404)

        user=auth.authenticate(username=data['username'],password=data['password'])
        if user is not None:
            auth.login(request,user)
            return JsonResponse({'message': "Logged In Successfully!"},status=200)
        else:
            return JsonResponse({'message': "Invalid Credentials"},status=400)
    return JsonResponse({'message': "error:Provide Credentials"},status=400)
  
def vote(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method=='GET':
                items=Item.objects.all()
                serializers=ItemStaffSerializer(items,many=True)
                return JsonResponse(serializers.data,safe=False)
        else:
            if request.method=='GET':
                items=Item.objects.all()
                serializers=ItemSerializer(items,many=True)
                return JsonResponse(serializers.data,safe=False)
        
        
    else:
        return JsonResponse({'message': "You need to login first"},status=400)
@csrf_exempt
def voting(request,title):
    if request.method=='POST':
        if request.user.is_authenticated:
            if request.user.is_staff:
                return JsonResponse({'message': "Admin Cannot Vote"},status=400)
            else:
                voted_item=get_object_or_404(Item,title=title)
                username=request.user.username
                user = get_object_or_404(User,username=username)
                if user.userprofile.has_voted==True:
                    return JsonResponse({'message': "You Have Already Voted"},status=400)
                else:
                    voted_item.count+=1
                    
                    user.userprofile.has_voted=True
                    user.userprofile.voted_item=voted_item.title
                    user.userprofile.save()
                    voted_item.save()
                    return JsonResponse({'message': "Voted Successfully!"},status=200)
        else:
            return JsonResponse({'message': "You need to login to vote!"},status=400)

@csrf_exempt
def AddItem(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method=='POST':
                data=JSONParser().parse(request)
                data['count']=0
                serializers=ItemSerializer(data=data)
                if serializers.is_valid():
                    serializers.save()
                    return JsonResponse({'message': "Item Added!"},status=201)
                return JsonResponse(serializers.errors,status=400)
            else:
                return JsonResponse({'message': "Post Item name"},status=400)
        else:
            return JsonResponse({'message': "Not Authorized!"},status=400)
    else:
        return JsonResponse({'message': "You need to login as ADMIN"},status=400)

@method_decorator(csrf_exempt,name='dispatch')
@parser_classes((MultiPartParser,FormParser))
class FileUploadView(APIView):
    def post(self, request):
        #display_picture=request.FILES['display_picture']
        #print(display_picture)
        data=json.loads(request.data['data'])
        serializer = UserSerializer(data=data)
        #username=data['username']
        #serializers2=UserprofileSerializer(data=request.FILES)
        #print(str(serializer.is_valid()) +" and "+ str(serializers2.is_valid()))
        if serializer.is_valid():# and serializers2.is_valid():
            serializer.save()
            #username=serializer.validated_data['username']
            #print(str(User.objects.get(username=username))+' '+ str(type(User.objects.get(username=username))))
            #userprofile=Userprofile(user=User.objects.get(username=username),display_picture=serializers2.save())
            #userprofile.save()
            return JsonResponse({'message': "Registered Successfully!"},status=201)
        return JsonResponse(serializer.errors,status=400)
        

@csrf_exempt
def logout(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            auth.logout(request)
            return JsonResponse({'message': "Logged Out Successfully!"},status=200)
        else:
            return JsonResponse({'message': "error:Post request to Log Out"},status=400)
    else:
        return JsonResponse({'message': "Already Logged Out"},status=400)
