from django.shortcuts import render
from rango.forms import CategoryForm
from django.http import HttpResponse
#Import the Category model
from rango.models import Category
#Import Page
from rango.models import Page
from rango.forms import PageForm
# Import Userform
from rango.forms import UserForm, UserProfileForm
# Import Login
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary
    # that will be passed to the template engine.
    category_list=Category.objects.order_by('-likes')[:5]
    page_list=Page.objects.order_by('-views')[:5]
    context_dict={'categories': category_list, 'pages': page_list}

    #Render the response and send it back!
    return render(request,'rango/index.html', context_dict)
def about(request):
    #return HttpResponse("Rango says this tutorial has been put together by Lei Wang.<br/><a href ='/rango/about'>About</a></br><a href='/rango/'>Index</a>")
    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser'
    print(request.user)
    return render(request, 'rango/about.html', {})

def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict= {}
    try:
            # Can we find a category name slug with the given name?
            # If we can't, the .get() method raises a DoesNotExist exception.
            # So the .get() method returns one model instance or raises an exception
            category = Category.objects.get(slug=category_name_slug)

            # Retrieve all of the associated pages.
            # Note that filter() will return a list of page objects or an empty list
            pages= Page.objects.filter(category=category)

            #Add our results list to the template context under name pages.
            context_dict['pages']=pages
            # We also add the category object from
            # the database to the context dictionary.
            # We'll use this in the template to verify that the category exists
            context_dict['category']=category
    except Category.DoesNotExist:
            # We get here if we didn't find the specified category.
            # Don't do anything
            #the template will display the "no category" message for us
            context_dict['category']=None
            context_dict['pages']=None

        #Go render the response and return it to the client
    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    form = CategoryForm()

    #A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        #Have we been provided with a valid form?
        if form.is_valid():
            #Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved
            # We could give a confirmation message
            # But since the most recent category added is on the index page
            # Then we can direct the user back to the index page.

            return index(request)
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)

    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
        try:
            category = Category.objects.get(slug=category_name_slug)
        except Category.DoesNotExist:
            category = None

        form = PageForm()
        if request.method =='POST':
            form = PageForm(request.POST)
            if form.is_valid():
                if category:
                    page = form.save(commit=False)
                    page.category = category
                    page.views =0
                    page.save()
                    return show_category(request, category_name_slug)
                else:
                    print(form.errors)
        context_dict={'form':form, 'category': category}
        return render(request, 'rango/add_page.html', context_dict)

# Processing form input data
def register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
    # Attempt to grab information from the raw form information.
    # Note that we make use of both UserForm and UserProfileForm.
        user_form= UserForm(data=request.POST)
        profile_form= UserProfileForm(data=request.POST)
    # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            # put it in the UserProfile model.
            if 'picture' in request.FILES:
                 profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    # Render the template depending on the context.
    return render(request,
    'rango/register.html',
    {'user_form': user_form,
    'profile_form': profile_form,
    'registered': registered})

# Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html', {})

# Check Login
def some_view(request):
    if not request.user.is_authenticated():
        return HttpResponse("You are logged in.")
    else:
        return HttpResponse("You are not logged in.")
    
@login_required
def restricted(request):
    return render(request, 'rango/restricted.html',{})
    
# Logout
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('index'))
    



                    
            






            
            
            
