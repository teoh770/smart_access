import os
import sys, time
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template.context_processors import csrf
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from smart_access.forms import userForm
from smart_access.models import User
from smart_access.models import log
from smart_access import faceRec
from smart_access import eigenfaces
from django.core import serializers
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth import logout

def index(request):
    if len(os.listdir('media/smart_access/library/')) != 1 or len(os.listdir('media/smart_access/library/')) > 1:
        filename = os.listdir('media/smart_access/library/')[1]
        pyf = faceRec.PyFaces()
        userID =  pyf.face_recognition(1,'media/smart_access/library/',30,'media/smart_access/library/'+filename)
    return render(request, 'smart_access/index.html')

def passkey_auth(request):
    if request.method == 'POST':
        if request.POST['passkey'] == 'abc123':
            return redirect('/granted')
        else:
            return render(request, 'smart_access/wrongpasskey.html')
    else:
        return render(request, 'smart_access/passkey.html')


#this function is to register new user
def register(request):
    if not request.user.is_authenticated():
        return redirect( '/login')
    else:
        if request.method == 'POST':
            form = userForm(request.POST)
            #form data will assign into temp object
            obj = form.save(commit=False)
            #save the object into database
            obj.save()
            #userId will save into session for the use of updloading the user image into library
            request.session['image_id'] =  obj.id
            return render(request, 'smart_access/capture_dataset.html')
        else:
            return render(request, 'smart_access/register.html')



def add_dataset(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'smart_access/capture_dataset.html')

def validate(request):
    if len(os.listdir('media/smart_access/library/')) == 1 or len(os.listdir('media/smart_access/library/')) < 1:
        return redirect( '/')
    else:
        c = {}
        c.update(csrf(request))
        return render(request, 'smart_access/validation.html', c)


def access_granted(request):
    return render(request, 'smart_access/granted.html')

#this function is to add new user image to library
def upload_dataset(request):
    if request.is_ajax():
        if request.method == 'POST':
            if request.session['image_id']:
                image_id = request.session['image_id']
                #get the image from form
                data = request.FILES['file']
                path = 'smart_access/library/'+str(image_id)+'.gif'
                #store the image into specific path
                default_storage.save(path, ContentFile(data.read()))
                return HttpResponse('True')
            else:
                return render(request, 'smart_access/index.html')
        else:
            return render(request, 'smart_access/index.html')
    else:
        return render(request, 'smart_access/index.html')

#this function is to verify user
def verify_user(request):
    if request.is_ajax():
        if request.method == 'POST':
            data = request.FILES['file']
            path = 'smart_access/temp/temp.gif'
            default_storage.save(path, ContentFile(data.read()))
            #assign face recognition class into instance
            pyf = faceRec.PyFaces()
            #call face recognition process to work and it will return the userID
            userID =  pyf.face_recognition(1,'media/smart_access/library/',30,'media/smart_access/temp/temp.gif')
            #after the recognition process the temp face image file will be deleted
            default_storage.delete(path)
            if userID != False:
                #if the user is recognized
                #will use the userId to query database to get the user information
                authenticated = User.objects.get(id__exact=userID)
                #log will save into database
                authLog = log(user = authenticated, status = True)
                authLog.save()
                #the user information will serialize into json object and pass back to frontend
                return HttpResponse(serializers.serialize("json", [authenticated]))
            else:
                authLog = log( status = False)
                authLog.save()
                #if the user not found, will return false to fronend
                return JsonResponse({'error':True})

        else:
            return render(request, 'smart_access/index.html')
    else:
        return render(request, 'smart_access/index.html')

def send_email(request):
    message = "Please response ASAP."
    subject = "Emergency"
    send_mail(subject, message, 'fyptestingw13044808@gmail.com', ['teoh770@gmail.com'], fail_silently=False)
    return render(request, 'smart_access/emergency.html')

def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('/admin')
            else:
                context_dict = {'error': 'Your admin account is disabled!'}
                return render_to_response('smart_access/login.html', context_dict, context)
        else:
            context_dict = {'error': 'Incorrect username/password!'}

            print "Invalid login details: {0}, {1}".format(username, password)
            return render_to_response('smart_access/login.html', context_dict, context)
    else:
        return render_to_response('smart_access/login.html', {}, context)

def user_logout(request):
    logout(request)
    return redirect('/')

def admin_panel(request):
    context = RequestContext(request)
    if not request.user.is_authenticated():
        return redirect( '/login')
    else:
        logList = log.objects.all()
        userList = User.objects.all()
        return render_to_response('smart_access/admin_panel.html', {'logList':logList, 'userList':userList}, context)
