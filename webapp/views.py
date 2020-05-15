from django.shortcuts import render

# Create your views here.
from django.contrib.contenttypes.models import ContentType
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt, csrf_protect


from rest_framework.parsers import MultiPartParser, JSONParser,FormParser, FileUploadParser
from django.core.files.storage import FileSystemStorage

from .models import File
from .serializers import FileSerializer
#from .forms import FileForm

from werkzeug.utils import secure_filename
import mimetypes
from django.utils.encoding import smart_str
import shutil
import os
from . import tools
from . import divider as dv
from . import encrypter as enc
from . import decrypter as dec
from . import restore as rst

UPLOAD_FOLDER = './uploads/'
UPLOAD_KEY = './key/'
ALLOWED_EXTENSIONS = set(['pem'])
a = ''

class ApiError(Exception):
    """A Custom API Error Exception Handling class"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "APIError Occured : Status Code = {} ".format(self.status)


class fileList(APIView):
    parser_classes = (FileUploadParser)
    
    def get(self, request):
        fileList = File.objects.all()
        serializer = FileSerializer(fileList, many = True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



'''def encrypt(request):
    if request.method =='POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
    return render(request, 'encrypt.html')

def encrypt2(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('')
    else:
        form = FileForm()
    return render(request, 'encrypt2.html', {
        'form':form
    })'''

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def start_encryption(request):
	dv.divide()
	tools.empty_folder('uploads')
	enc.encrypter()
	return render(request, 'success.html')

def start_decryption(request):
	dec.decrypter()
	tools.empty_folder('key')
	rst.restore()
	return render(request,'restore_success.html')

def return_key(request):
	list_directory = tools.list_dir('key')
	filename = './key/' + list_directory[0]
	path = filename
	fl = open(path, 'r')
	mime_type, _ = mimetypes.guess_type(path)
	
	response = HttpResponse(fl, content_type=mime_type)
	response['Content-Disposition'] = "attachment; filename=%s" % a+'.pem'
	return response

	#return shutil.copyfile(filename ,r'C:/Users/saura/Downloads/My_Key.pem' )  #Here Might be a prblem

def return_file(request):
	list_directory = tools.list_dir('restored_file')
	filename = './restored_file/' + list_directory[0]
	print("****************************************")
	print(list_directory[0])
	print("****************************************")
	path = filename
	fl = open(path, 'rb')
	mime_type, _ = mimetypes.guess_type(path)
	
	response = HttpResponse(fl, content_type=mime_type)
	response['Content-Disposition'] = "attachment; filename=%s" % list_directory[0]
	return response


def downloads(request):
	return render(request,'download.html')

@csrf_exempt
def call_page_upload(request):
	return render(request,'upload.html')

def back_home(request):
	tools.empty_folder('key')
	tools.empty_folder('restored_file')
	return render(request, 'index.html')

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def upload_file(request):
	global a
	tools.empty_folder('uploads')
	if request.method == 'POST':

		# check if the post request has the file part
		if 'file' not in request.FILES:
			messages.add_message(request, messages.WARNING, "No file part")
			#flash('No file part')
			return HttpResponseRedirect('/request/url/')
		file = request.FILES['file']
		a = os.path.splitext(file.name)[0]
		if file.name == '':
			messages.add_message(request, messages.WARNING, "No selected file")
			return HttpResponse("NO FILE SELECTED")
		if file:
			filename = file.name
			
			#this code copies the selected file from path given to the upload folder
			shutil.copy('./Dataset/'+filename , UPLOAD_FOLDER )
			
			#original code follows here  
			"""os.path.join('UPLOAD_FOLDER', file.name)
			file.close()
			path = './uploads'
			dirs = os.listdir(path)
			print(dirs)"""
			return start_encryption(request)
		return HttpResponse("Invalid File Format !")

@csrf_exempt
def upload_key(request):
	tools.empty_folder('key')
	if request.method == 'POST':
		if 'file' not in request.FILES:
			messages.add_message(request, messages.WARNING, "No file part")
			return HttpResponseRedirect('/request/url/')
		file = request.FILES['file']
		if file.name == '':
			messages.add_message(request, messages.WARNING, "No selected file")
			return HttpResponse("NO FILE SELECTED")
		if file and allowed_file(file.name):
			filename = file.name
			print(filename)
			shutil.copy('C:/Users/saura/Downloads/'+ filename , UPLOAD_KEY )
			return start_decryption(request)
		return HttpResponse("Invalid File Format !")
