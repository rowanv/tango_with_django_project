from django.shortcuts import render
from django.http import HttpResponse

from rango.models import Category, Page


def index(request):
	# Query the database for a list of ALL categories currently stored
	# Order the categories by no. likes in descending order
	# Retrieve the top 5 only - or all if less than 5
	# Place the list in our context_dict dictionary which will be passed to the template engine.
	category_list = Category.objects.order_by('-likes')[:5]
	context_dict = {'categories': category_list}

	return render(request, 'rango/index.html', context_dict)

def about(request):
	context_dict = {'boldmessage': 'This is the about page!'}
	return render(request, 'rango/about.html', context_dict)

def category(request, category_name_url):
	context_dict = {}

	try:
		category = Category.objects.get(slug=category_name_url)
		context_dict['category_name'] = category.name
		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
		context_dict['category'] = category
	except Category.DoesNotExist:
		pass
	return render(request, 'rango/category.html', context_dict)