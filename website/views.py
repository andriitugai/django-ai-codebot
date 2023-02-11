import os
import openai

from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

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
			return render(request, 'suggest.html', {'lang_list':lang_list, 'response': fixed_code, 'lang': lang})

		except Exception as e:
			return render(request, 'suggest.html', {'lang_list':lang_list, 'code': e, 'lang': lang})

	return render(request, 'suggest.html', {'lang_list':lang_list})
