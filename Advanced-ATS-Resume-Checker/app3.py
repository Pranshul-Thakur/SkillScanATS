from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)

# Allow all origins for debugging, can be restricted to specific domains later
CORS(app, resources={r"/*": {"origins": "*"}})

ROLE_URLS = {
    "Backend Engineer": "https://www.geeksforgeeks.org/backend-developer-interview-questions-and-answers/",
    "AI/ML Engineer": "https://www.geeksforgeeks.org/machine-learning-interview-questions/",
    "MLOps Engineer": "https://www.geeksforgeeks.org/comprehensive-mlops-interview-questions-from-basic-to-advanced/",
    "SDE": "https://www.geeksforgeeks.org/top-50-software-engineering-interview-questions-and-answers/",
    "Frontend Engineer": "https://www.geeksforgeeks.org/front-end-developer-interview-questions/",
    "Fullstack Engineer": "https://www.geeksforgeeks.org/full-stack-developer-interview-questions-and-answers/",
    "Data Analyst": "https://www.geeksforgeeks.org/data-analyst-interview-questions-and-answers/",
    "Data Scientist": "https://www.geeksforgeeks.org/data-science-interview-questions-and-answers/",
    "HR Interview Questions": "https://www.geeksforgeeks.org/top-10-traditional-hr-interview-questions-and-answers/"
}
def get_interview_questions(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        return ["Failed to fetch questions. Please try again later."]
    
    soup = BeautifulSoup(response.text, 'html.parser')
    questions = []
    
    if(url == "https://www.geeksforgeeks.org/top-10-traditional-hr-interview-questions-and-answers/"):
        for h3 in soup.find_all("h2"):
            text = h3.get_text(strip=True)
            if "?" or "." in text and len(text) > 5:
                questions.append(text)
    
        return questions[:10]

    for h3 in soup.find_all("h3"):
        text = h3.get_text(strip=True)
        if "?" or "." in text and len(text) > 5:
            questions.append(text)
    
    return questions[:20]

def get_questions_for_role(role):
    if role not in ROLE_URLS:
        return {"error": "Invalid role selected."}
    
    url = ROLE_URLS[role]
    questions = get_interview_questions(url)
    
    return {
        "role": role,
        "questions": questions
    }

@app.route('/get-interview-questions', methods=['POST'])
def fetch_interview_questions():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    role = data.get('role', '')
    
    if not role:
        return jsonify({"error": "No role specified"}), 400
    
    result = get_questions_for_role(role)
    return jsonify(result)

@app.route("/")
def home():
    return "Flask is running!"

if __name__ == "__main__":
    app.run(debug=True, port=5001)
