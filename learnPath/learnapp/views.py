from django.shortcuts import render
from .ai_suggestions import get_ai_suggestions, get_coursera_courses

def index(request):
    return render(request, 'learnapp/index.html')

def questions(request):
    return render(request, 'learnapp/questions.html')

def generate_learning_path(request):



    if request.method == 'POST':
        # Process form data
        interests = request.POST.getlist('interests')
        ai_suggestions = get_ai_suggestions(interests)
        coursera_courses = get_coursera_courses(interests[0], 'access_token')  # You'll need to handle access token
        
        context = {
            'ai_suggestions': ai_suggestions,
            'coursera_courses': coursera_courses,
        }
        return render(request, 'learnapp/results.html', context)
    return render(request, 'learnapp/questions.html')
