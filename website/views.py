import os
import openai

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from .models import Code

lang_list = [
		'c', 'clike', 'cpp', 'csharp', 'css', 'dart', 'django', 
		'go', 'go-module', 'html', 'java', 'javascript', 'markup', 
		'markup-templating', 'mongodb', 'objectivec', 'perl', 'php', 
		'python', 'ruby', 'rust', 'scala', 'sql', 'toml', 
		'typescript', 'typoscript', 'yaml'
	]

# Create your views here.
def home(request):
	
	if request.method == "POST":
		code = request.POST['code']
		lang = request.POST['lang']

		if lang == "Select Programming Language":
			messages.success(request, "You forgot to select a programming Language!")
			return render(request, 'home.html', {'lang_list':lang_list, 'code': code, 'lang': lang})

		# OPEN AI!
		openai.api_key = os.environ['OPENAI_SECRET_KEY']
		# Create OpenAI instance
		openai.Model.list()
		# Make an OpenAI request
		try:
			response = openai.Completion.create(
				engine = 'text-davinci-003',
				prompt = f"Respond only with code. Fix this {lang} code: \n\n{code}",
				temperature = 0,
				max_tokens = 1500,
				top_p = 1.0,
				frequency_penalty = 0.0,
				presence_penalty = 0.0,
				)
			# parse the response
			fixed_code = (response["choices"][0]["text"]).strip()

			# Save fixed code to DataBase
			record = Code(question=code, code_answer=fixed_code, language=lang, user=request.user)
			record.save()

			return render(request, 'home.html', {'lang_list':lang_list, 'response': fixed_code, 'lang': lang})

		except Exception as e:
			return render(request, 'home.html', {'lang_list':lang_list, 'code': e, 'lang': lang})

	return render(request, 'home.html', {'lang_list':lang_list})

def info(request):
	return render(request, 'info.html', {})


def suggest(request):
		
	if request.method == "POST":
		code = request.POST['code']
		lang = request.POST['lang']

		if lang == "Select Programming Language":
			messages.success(request, "You forgot to select a programming Language!")
			return render(request, 'suggest.html', {'lang_list':lang_list, 'code': code, 'lang': lang})

		# OPEN AI!
		openai.api_key = os.environ['OPENAI_SECRET_KEY']
		# Create OpenAI instance
		openai.Model.list()
		# Make an OpenAI request
		try:
			response = openai.Completion.create(
				engine = 'text-davinci-003',
				prompt = f"Respond only with code. {code}",
				temperature = 0,
				max_tokens = 1500,
				top_p = 1.0,
				frequency_penalty = 0.0,
				presence_penalty = 0.0,
				)
			# parse the response
			fixed_code = (response["choices"][0]["text"]).strip()

			# Save fixed code to DataBase
			record = Code(question=code, code_answer=fixed_code, language=lang, user=request.user)
			record.save()

			return render(request, 'suggest.html', {'lang_list':lang_list, 'response': fixed_code, 'lang': lang})

		except Exception as e:
			return render(request, 'suggest.html', {'lang_list':lang_list, 'code': e, 'lang': lang})

	return render(request, 'suggest.html', {'lang_list':lang_list})

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You have been logged in!")
		else:
			messages.success(request, "Error Logging In. Try Again.")
		return redirect('home')
	else:
		return render(request, 'home')

def logout_user(request):
	logout(request)
	messages.success(request, "You have been logged Out...")
	return redirect('home')

def register_user(request):
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(request, username=username, password=password)
			login(request, user)
			messages.success(request, "You have successfuly registered...")
			return redirect('home')
	else:
		form = SignUpForm()

	return render(request, 'register.html', {"form": form})


def past(request):
	if request.user.is_authenticated:
		code = Code.objects.filter(user_id=request.user.id)
		return render(request, 'past.html', {'code': code})
	messages.success(request, "You must be logged in...")
	return redirect('home')

def delete_past(request, past_id):
	past = Code.objects.get(pk=past_id)
	past.delete()
	messages.success(request, "Deleted Successfully...")
	return redirect('past')








