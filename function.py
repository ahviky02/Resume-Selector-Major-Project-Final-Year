import re
from PyPDF2 import PdfReader
import re


def extract_text_from_pdf(uploaded_file):
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def extract_skills_from_text(text):
    """
    This function is used for finding Programming languages skills.
    """

    # Define a regular expression pattern to match common Programming languages skills formats
    skills_pattern = r"\b(?:PHP|HTML|JavaScript|CSS|Laravel|Java|Matplotlib|Python|C|R|ReactJs|NodeJs)\b"

    # Find all matches of the Programming languages skills pattern in the text
    skills = re.findall(skills_pattern, text, flags=re.IGNORECASE)

    return set(skills)


def extract_degrees_from_text(text):
    """
    this function is used for find the Degrees
    """
    # Define a regular expression pattern to match common Degrees formats
    degree_pattern = r"\b(?:Ph\.?D\.?|M\.?S\.?|B\.?Sc\.?|MBA|MA|BA|BS|B\.?Tech\.?)\b"

    # Find all matches of the degree pattern in the text
    degrees = re.findall(degree_pattern, text, flags=re.IGNORECASE)

    return set(degrees)


def extract_place_from_text(text):
    """
    this function is used for find place
    """
    # find the all matches places
    place = [ent.text for ent in doc.ents if ent.label_ == "GPE"]

    return set(place)


def extract_emails_from_text(text):
    # Define the regular expression pattern for matching email addresses
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    # Find all matches of the email pattern in the text
    emails = re.findall(email_pattern, text)

    return set(emails)


def clean_resume(resume_text):
    clean_text = re.sub("http\S+\s*", " ", resume_text)
    clean_text = re.sub("RT|cc", " ", clean_text)
    clean_text = re.sub("#\S+", "", clean_text)
    clean_text = re.sub("@\S+", "  ", clean_text)
    clean_text = re.sub(
        "[%s]" % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), " ", clean_text
    )
    clean_text = re.sub(r"[^\x00-\x7f]", r" ", clean_text)
    clean_text = re.sub("\s+", " ", clean_text)
    return clean_text


def extract_mobile_numbers(text):
    # Regular expression pattern to match mobile numbers with optional country code "+91"
    # pattern = r"\b(?:(\d{10})|(\+91?\d{10}))\b"
    text = text.replace(" ", "")
    pattern = r"(?:\+\d{12}|\d{10})"
    # Find all matches in the text
    mobile_numbers = re.findall(pattern, text)
    # Return unique mobile numbers
    return set(mobile_numbers)
