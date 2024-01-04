import google.auth
from vertexai.preview.generative_models import GenerativeModel
from google.cloud.aiplatform_v1beta1.types.content import HarmCategory, SafetySetting

model = GenerativeModel("gemini-pro")

# Block only high probability harmful content
safety_settings = {
    HarmCategory.HARM_CATEGORY_UNSPECIFIED: SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_HARASSMENT: SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH,
}


def summarize_article(article: str) -> str:
    prompt = f"""
    Provide a brief summary for the following article in Vietnamese, use easy to understand language: 

    Article:
    {article}
    """
    responses = model.generate_content(
        prompt,
        stream=False,
        safety_settings=safety_settings,
        generation_config={
            "temperature": 0.1,
            "max_output_tokens": 512,
            "candidate_count": 1,
        }
    )

    return responses.text


def adsometer(article: str) -> str:
    prompt = f"""
    Please analyze the following article and assign it an appropriate rating based on the degree of promotional or advertising content it contains.

    Use this rating scale:

    Purely informational: The article contains no promotional or advertising elements.
    Neutral: The article contains a few minor promotional elements, but the primary focus is still on providing information.
    Highly promotional: The article is primarily focused on promoting a product, service, or brand, with information being secondary.

    Article:
    {article}

    Rating:
    """
    responses = model.generate_content(
        prompt,
        stream=False,
        safety_settings=safety_settings,
        generation_config={
            "temperature": 0.1,
            "max_output_tokens": 512,
            "candidate_count": 1,
        }
    )

    return responses.text


def hashtags_tokenization(article: str):
    prompt = f"""
    What are the hashtags of the following article? Output max 3 tags in comma-separated format, no further explanation.

    Article:
    {article}

    Tags:
    """
    responses = model.generate_content(
        prompt,
        stream=False,
        safety_settings=safety_settings,
        generation_config={
            "temperature": 0.1,
            "max_output_tokens": 1024,
            "candidate_count": 1,
        }
    )

    return responses.text
