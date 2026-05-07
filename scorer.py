import requests

API_URL = "https://antsy-eligibly-delay.ngrok-free.dev/analyze"

def get_score(resume_text, job_description):
    try:
        response = requests.post(API_URL, json={
            "resume": resume_text,
            "job_description": job_description
        })
        return response.json()["score"]
    except:
        return 0
