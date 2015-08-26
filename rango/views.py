from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm



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
		context_dict['category_name_slug'] = category.slug
	except Category.DoesNotExist:
		pass
	return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
	if request.method == 'POST':
		form = CategoryForm(request.POST)

		if form.is_valid():
			form.save(commit=True)
			return index(request)
		else:
			print(form.errors)
	else:
		form = CategoryForm()

	return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_url):

    try:
        cat = Category.objects.get(slug=category_name_url)
    except Category.DoesNotExist:
                cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_url)
        else:
            print(form.errors)
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat, 'category_name_slug': category_name_url}

    return render(request, 'rango/add_page.html', context_dict)

def register(request):
	context = RequestContext(request)

	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			profile.save()

			registered = True

		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = UserProfileForm
	return render_to_response('rango/register.html', {'user_form': user_form,
		'profile_form': profile_form, 'registered': registered}, context)

def user_login(request):
	context = RequestContext(request)

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/rango/')
			else:
				return HttpResponse('Your rango account is disabled.')
		else:
			print('Invalid login details: {0}, {1}'.format(username, password))
			return HttpResponse('Invalid login details supplied.')
	else:
		return render_to_response('rango/login.html', {}, context)


@login_required
def restricted(request):
	return HttpResponse('Since you are logged in, you can see this text!')

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/rango/')