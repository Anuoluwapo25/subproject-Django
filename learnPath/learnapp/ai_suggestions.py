import os
import google.generativeai as genai
import requests
import base64

# Use environment variables for API keys
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
COURSERA_APP_KEY = os.environ.get('COURSERA_APP_KEY')
COURSERA_APP_SECRET = os.environ.get('COURSERA_APP_SECRET')

def configure_genai():
    if not GEMINI_API_KEY:
        raise ValueError("Gemini API key not found. Please set the GEMINI_API_KEY environment variable.")
    genai.configure(api_key=GEMINI_API_KEY)

def get_ai_suggestions(interests):
    configure_genai()
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""For someone interested in {', '.join(interests)}, please provide:

1. Name:
  - Name of project


2. Overview:
   - Brief description of each selected technology
   - How these technologies relate to each other (if applicable)

3. Resources:
   - Types of courses or certifications that would be beneficial
   - Recommended books or online resources
   - Relevant communities or forums for support and networking

Please structure your responses for each section clearly with headers in bold and each points well structured for easy readability. can every link be accessible with an underline"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating AI suggestions: {str(e)}")
        return "Unable to generate AI suggestions at this time."

def get_coursera_access_token():
    url = "https://api.coursera.com/oauth2/client_credentials/token"
    auth_string = f"{COURSERA_APP_KEY}:{COURSERA_APP_SECRET}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_auth}"
    }
    data = {"grant_type": "client_credentials"}
    
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.RequestException as e:
        print(f"Error obtaining Coursera access token: {str(e)}")
        return None

def get_coursera_courses(subject, access_token):
    url = "https://api.coursera.org/api/courses.v1"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": "search", "query": subject, "limit": 5, "fields": "name,slug"}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        courses = response.json().get("elements", [])
        return [{"name": course["name"], "url": f"https://www.coursera.org/learn/{course['slug']}"} for course in courses]
    except requests.RequestException as e:
        print(f"Error fetching Coursera courses: {str(e)}")
        return []