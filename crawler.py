import re

import requests
from readability.readability import Document


def clean_paragraphs(text):
    """Cleans up paragraphs with multiple newlines, preserving intended structure.

    Args:
        text: The input text string to be cleaned.

    Returns:
        The cleaned text string with single newlines between paragraphs.
    """

    # Preserve double newlines that likely indicate intentional paragraph breaks
    cleaned_text = re.sub(r"\n{3,}", "\n\n", text)  # Replace 3 or more newlines with 2

    # Collapse remaining consecutive newlines into single newlines
    cleaned_text = re.sub(r"\n{2,}", "\n", cleaned_text)

    return cleaned_text


def readability_text(url: str) -> str:
    """Convert html article to text"""

    # Get the html code of the page
    clean = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0 Safari/537.36',
        'language': 'en-US,en;q=0.9,vi;q=0.8'
    }
    response = requests.get(url, headers=headers, timeout=10)
    document = Document(response.text)
    doc = document.title()
    elem = document.summary()

    title = clean_paragraphs(re.sub(clean, '', doc))
    content = clean_paragraphs(re.sub(clean, '', elem))

    return f"""
    {title}
    {content}
    """
