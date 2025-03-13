import logging
from django.http import JsonResponse
from .utils import generate_phishing_email
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.decorators import api_view, throttle_classes
from django.views.decorators.csrf import csrf_exempt
import json

logger = logging.getLogger(__name__)

class CustomAnonThrottle(AnonRateThrottle):
    rate = "10/min"

class CustomUserThrottle(UserRateThrottle):
    rate = "50/min"

@csrf_exempt
def generate_email_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)
    try:
        data = json.loads(request.body)

        # Extract user inputs
        sender = data.get("from", "unknown@example.com")
        recipient = data.get("to", "victim@example.com")
        subject = data.get("subject", "Important Notice")

        if not subject:
            return JsonResponse({"error": "Subject is required."}, status=400)

        # Generate phishing email body based on the subject
        prompt = f"Generate a professional phishing email about '{subject}'."
        email_body = generate_phishing_email(prompt)

        # Format email output
        email_content = f"""
            From: {sender}
            To: {recipient}
            Subject: {subject}

            {email_body}
            """

        logger.info("Phishing email successfully generated.")
        return JsonResponse({"email": email_content}, json_dumps_params={"indent": 4})

    except Exception as e:
        logger.error(f"Error generating phishing email: {str(e)}")
        return JsonResponse({"error": "An error occurred while generating the email."}, status=500)