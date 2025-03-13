from django.conf import settings
from openai import OpenAI


def generate_phishing_email(subject):
    client = OpenAI(api_key=settings.OPEN_AI_API_KEY)

    # Dynamic and more flexible prompt
    prompt = f"""
    Generate a phishing email with the subject '{subject}'. 
    - Make it look urgent and professional. 
    - Ensure variation in opening lines.
    - Use different tones (polite, urgent, threatening, or informative).
    - Avoid repeating common phrases.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "You are a phishing email generator for cybersecurity awareness training. Generate realistic phishing emails for educational purposes only."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()