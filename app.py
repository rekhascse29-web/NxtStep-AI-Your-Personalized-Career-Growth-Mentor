from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from groq import Groq
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "../frontend"),
    static_folder=os.path.join(BASE_DIR, "../frontend/static")
)
CORS(app)

# -----------------------------------
# Load Environment Variables
# -----------------------------------

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(BASE_DIR, ".env"))
API_KEY = os.getenv("GROQ_API_KEY")

print("Current Directory:", os.getcwd())
print("BASE_DIR:", BASE_DIR)
print("ENV Exists:", os.path.exists(os.path.join(BASE_DIR, ".env")))
print("API KEY:", API_KEY)

if not API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

# -----------------------------------
# Groq Client
# -----------------------------------

client = Groq(api_key=API_KEY)

# -----------------------------------
# Flask App
# -----------------------------------

# -----------------------------------
# Home Route
# -----------------------------------
from flask import render_template

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/assessment")
def assessment():
    return render_template("assessment.html")

@app.route("/loading")
def loading():
    return render_template("loading.html")

@app.route("/result")
def result():
    return render_template("result.html")

# -----------------------------------
# Test Route
# -----------------------------------

@app.route("/test")
def test():

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": "Say Hello"
                }
            ]
        )

        return jsonify({
            "success": True,
            "response": response.choices[0].message.content
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })

# -----------------------------------
# Analyze Route
# -----------------------------------

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        data = request.get_json()

        prompt = f"""
You are an expert AI Career Counselor.

Analyze the following student profile and provide a professional career guidance report.

Student Details

Name:
{data.get("name")}

Education:
{data.get("education")}

Career Goal:
{data.get("career_goal")}

Technical Skills:
{", ".join(data.get("skills", []))}

Areas to Improve:
{data.get("improvement")}

Learning Style:
{data.get("learning_style")}

Generate a beautiful career report in VALID HTML.

Rules:
- Use only HTML tags.
- Do NOT use Markdown (** or *).
- Use <h2> for title.
- Use <h3> for section headings.
- Use <p> for paragraphs.
- Use <ul><li> for bullet points.
- Highlight important keywords using <strong>.
- Keep the report clean, professional and modern.
- Do not include ```html``` or code blocks.

Report Structure:

<h2>Career Guidance Report for {data.get("name")}</h2>

1. Career Summary

2. Best Career Roles (5)

3. Skill Gap Analysis

4. Recommended Technologies

5. 12-Month Learning Roadmap

6. Recommended Certifications

7. Resume Improvement Tips

8. Interview Preparation Strategy

9. Personalized Final Career Advice

Give detailed and practical suggestions.
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert AI Career Counselor."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1200
        )

        answer = response.choices[0].message.content

        return jsonify({
            "success": True,
            "response": answer
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# -----------------------------------
# Run Server
# -----------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)