import fitz  # PyMUPDF
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def extract_text_from_pdf(uploaded_file):
    """
    Extract text from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF.
    
    """

    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    text = ""
    for page in doc:
        text += page.get_text()
    return text

def ask_openai(prompt, max_tokens=500):
    """
    Ask OpenAI a question and return the response.

    Args:
        prompt (str): The question to ask.
        max_tokens (int): The maximum number of tokens to generate.

    Returns:
        str: The response from OpenAI.

    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
            "role": "system",
            "content": "You are a helpful assistant."
            },
            {
            "role": "user",
            "content": prompt
            }
        ],
        temperature=0.5,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content





