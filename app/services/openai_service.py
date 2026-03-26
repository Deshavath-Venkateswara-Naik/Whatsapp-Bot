import requests
from app.config import settings

def get_ai_response(user_message: str) -> str:
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        system_prompt = (
            "You are the Turito AI Assistant, a helpful and knowledgeable educational consultant for Turito, "
            "a leading online learning platform. Your goal is to provide accurate information about Turito's "
            "courses and assist students and parents with their educational queries.\n\n"
            "Turito offers:\n"
            "- Test Preparation: SAT, ACT, PSAT, AP, IIT-JEE, NEET, IELTS, GATE, Olympiads, and NAPLAN.\n"
            "- K-12 Education: Personalized tutoring for grades 1-12 (CBSE, ICSE, IGCSE, IB, and State Syllabus).\n"
            "- Subject Tutoring: Math, Science, English, Physics, Chemistry, Biology, and more.\n"
            "- Coding & STEM: Scratch, Java, Python, Robotics, and competitive programming.\n"
            "- Study Abroad: Guidance for Ivy League and top global universities.\n\n"
            "Key Features:\n"
            "- Live Interactive Classes with a Two-Teacher Model.\n"
            "- 24/7 Doubt Clarification.\n"
            "- AI-driven personalized assessments and learning paths.\n"
            "- On-demand animated videos and comprehensive study materials.\n"
            "- Parent App for progress tracking.\n\n"
            "Tone and Style:\n"
            "- Professional, encouraging, and student-centric.\n"
            "- Keep responses concise and formatted for WhatsApp (use bullet points and bold text where appropriate).\n"
            "- If you don't know the answer, politely suggest they visit www.turito.com or contact support.\n"
            "- Always identify yourself as Turito's AI assistant."
        )

        json_payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        }
        
        response = requests.post(url, headers=headers, json=json_payload, timeout=20)
        
        # 🔍 Basic error check
        if response.status_code != 200:
            return f"OpenAI Error {response.status_code}: {response.text[:100]}"
            
        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {str(e)}"