from django.shortcuts import render, redirect, get_object_or_404
import logging
from .models import BlogPost
from django.core.paginator import Paginator
from django.db.models import Q
from .utils import validate_user_data
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_protect
from django_ratelimit.decorators import ratelimit
from django.contrib.auth.decorators import login_required

# Create your views here.

logger = logging.getLogger(__name__)


# Home view
def home(request):
    current_page = 'home'
    query = request.GET.get('q')

    if query:
        blogs_list = BlogPost.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by('-publication_date')
    else:
        blogs_list = BlogPost.objects.all().order_by('-publication_date')

    paginator = Paginator(blogs_list, 10)  # Show 10 blog posts per page
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)
    
    context = {
        'current_page': current_page,
        'blogs': blogs,
        'query': query,
    }
    return render(request, 'home.html', context)


# Register view
@csrf_protect
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def register_view(request):
    current_page = 'register'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # Validate user data
        error_message = validate_user_data(username, email, password, confirm_password)
        if error_message:
            messages.error(request, error_message)
            return render(request, 'register.html')

        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )

            # Authenticate and login user
            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                logger.info(f"User {user.username} Registered up successfully.")
                messages.success(request, 'Registered successfully and logged in.')
                return redirect('home')
            else:
                messages.error(request, 'Authentication failed. Please try logging in.')
        except ValidationError as e:
            logger.error(f"Validation error during registration: {str(e)}")
            messages.error(request, 'Validation error occurred during registration. Please try again.')
        except Exception as e:
            logger.exception(f"Failed to register user: {str(e)}")
            messages.error(request, 'An error occurred during registration. Please try again.')

    context = {'current_page': current_page}
    return render(request, 'register.html', context)


# Login view
@csrf_protect
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def login_view(request):
    current_page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Username does not exist.')
            return render(request, 'login.html')

        if user.check_password(password):
            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                logger.info(f"User {user.username} logged in successfully.")
                messages.success(request, 'Login successful')
                return redirect('home')
        else:
            messages.error(request, 'Incorrect password.')

    context = {'current_page': current_page}
    return render(request, 'login.html', context)

# Logout view
def logout_view(request):
    try:
        logout(request)
        messages.success(request, 'Logged out successfully')
    except Exception as e:
        logger.error(f"Failed to logout: {str(e)}")
        messages.error(request, f'Failed to logout')
    
    return redirect('home')

# Profile view
def profile(request):
    current_page = 'profile'
    user = request.user
    context = {
        'current_page': current_page,
        'user': user
    }
    return render(request, 'profile.html', context)

# Your blogs view
@login_required
def your_blogs_view(request):
    current_page = 'your_blogs'
    blogs = BlogPost.objects.filter(author=request.user).order_by('-id')
    context = {
        'current_page': current_page,
        'blogs': blogs
    }
    return render(request, 'your_blogs.html', context)


def blog_details_view(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)

    context = {
        'blog': blog
    }
    return render(request, 'blog_details.html', context)

# Add blog view
@login_required
def add_blog_view(request):
    current_page = 'add_blog'
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if not title or not content:
            messages.error(request, "Title and content are required.")
            return render(request, 'add_blogs.html', {'current_page': current_page})

        try:
            BlogPost.objects.create(
                title=title,
                content=content,
                author=request.user
            )
            messages.success(request, "Blog post added successfully!")
            return redirect('your_blogs')
        except Exception as e:
            logger.exception(f"Failed to add blog post: {str(e)}")
            messages.error(request, f"Failed to add blog post")

    context = {'current_page': current_page}
    return render(request, 'add_blogs.html', context)

# Edit blog view
@login_required
def edit_blog_view(request, blog_id):
    current_page = 'edit_blog'
    blog = get_object_or_404(BlogPost, id=blog_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if not title or not content:
            messages.error(request, "Title and content are required.")
            return render(request, 'edit_blog.html', {'blog': blog})

        try:
            blog.title = title
            blog.content = content
            blog.save()
            messages.success(request, "Blog post updated successfully!")
            return redirect('your_blogs')
        except Exception as e:
            logger.exception(f"Failed to edit blog post: {str(e)}")
            messages.error(request, f"Failed to edit blog post")

    context = {
        'current_page': current_page,
        'blog': blog
        }
    return render(request, 'edit_blog.html', context)

# Delete blog view
@login_required
def delete_blog_view(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    try:
        blog.delete()
        messages.success(request, "Blog post deleted successfully!")
    except Exception as e:
        logger.exception(f"Failed to delete blog post: {str(e)}")
        messages.error(request, f"An error occurred")
    return redirect('your_blogs')