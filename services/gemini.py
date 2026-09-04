import google.generativeai as genai


def configure_gemini(api_key, model_name="gemini-3.7-flash"):
    """
    Configure Gemini and return a GenerativeModel.
    """

    if not api_key:
        return None

    genai.configure(api_key=api_key)

    return genai.GenerativeModel(model_name)


def generate_decision(model, prompt):
    """
    Send one decision-intelligence request to Gemini.
    """

    if not model:
        return None, "no_api_key"

    try:

        response = model.generate_content(prompt)

        if not response or not response.text:
            return None, "empty_response"

        return response.text, "success"

    except Exception as error:

        error_text = str(error).lower()

        if "429" in error_text or "quota" in error_text:
            return None, "quota"

        return None, "error"