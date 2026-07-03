import requests

from services.local_ai_engine import (
    analyze_candidate
)

# ==========================================
# COLAB AI API
# ==========================================

COLAB_API_URL = "https://antsy-eligibly-delay.ngrok-free.dev/analyze"

# ==========================================
# HYBRID AI ENGINE
# ==========================================

def analyze_resume_with_ai(

    resume_text,

    job_description
):

    payload = {

        "resume": resume_text,

        "job_description": job_description
    }

    try:

        response = requests.post(

            COLAB_API_URL,

            json=payload,

            timeout=20
        )

        if response.status_code == 200:

            return response.json()

        else:

            print("COLAB ENGINE FAILED")

            print(response.text)

            print("USING LOCAL AI ENGINE")

            return analyze_candidate(

                resume_text,

                job_description
            )

    except Exception as e:

        print("COLAB CONNECTION ERROR")

        print(str(e))

        print("USING LOCAL AI ENGINE")

        return analyze_candidate(

            resume_text,

            job_description
        )