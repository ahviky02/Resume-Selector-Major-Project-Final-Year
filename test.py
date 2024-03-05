from library import *
import pickle
import re
import nltk
from function import *
import pandas as pd


nltk.download("punkt")
nltk.download("stopwords")
# loading models
clf = pickle.load(open("clf.pkl", "rb"))
tfidf = pickle.load(open("tfidf.pkl", "rb"))


def main():
    # Set page to full width
    st.set_page_config(layout="wide")

    st.markdown("<h2>Resume Screening App</h2>", unsafe_allow_html=True)

    # create tab menu
    pages = ["Resume", "Data", "Requirements", "About Us"]
    Resume, Data, Requirements, About = st.tabs(pages)

    with Resume:
        st.markdown("<h4>Upload Resume</h4>", unsafe_allow_html=True)
        uploaded_files = st.file_uploader(
            "Choose files",
            type=["txt", "pdf"],
            accept_multiple_files=True,
        )

        for uploaded_file in uploaded_files:
            if uploaded_file is not None:
                try:
                    resume_bytes = uploaded_file.read()
                    resume_text = resume_bytes.decode("utf-8")
                except UnicodeDecodeError:
                    # If UTF-8 decoding fails, try decoding with 'latin-1'
                    resume_text = resume_bytes.decode("latin-1")

                cleaned_resume = clean_resume(resume_text)
                input_features = tfidf.transform([cleaned_resume])
                prediction_id = clf.predict(input_features)[0]
                # st.write(prediction_id)

                # Map category ID to category name
                category_mapping = {
                    15: "Java Developer",
                    23: "Testing",
                    8: "DevOps Engineer",
                    20: "Python Developer",
                    24: "Web Designing",
                    12: "HR",
                    13: "Hadoop",
                    3: "Blockchain",
                    10: "ETL Developer",
                    18: "Operations Manager",
                    6: "Data Science",
                    22: "Sales",
                    16: "Mechanical Engineer",
                    1: "Arts",
                    7: "Database",
                    11: "Electrical Engineering",
                    14: "Health and fitness",
                    19: "PMO",
                    4: "Business Analyst",
                    9: "DotNet Developer",
                    2: "Automation Testing",
                    17: "Network Security Engineer",
                    21: "SAP Developer",
                    5: "Civil Engineer",
                    0: "Advocate",
                }

                category_name = category_mapping.get(prediction_id, "Unknown")

                st.write("Predicted Category:", category_name)

                # Extract text from the PDF
                text = extract_text_from_pdf(uploaded_file)

                Email = extract_emails_from_text(text)

                Degree = extract_degrees_from_text(text)

                Skills = extract_skills_from_text(text)

                mobile_numbers = extract_mobile_numbers(text)

                st.write("Email:", Email)
                st.write("Degree:", Degree)
                st.write("Skills:", Skills)
                st.write("Mobile Number:", mobile_numbers)

    with Requirements:
        st.markdown("<h4>Fill Requiremets </h4>", unsafe_allow_html=True)
        skill = st.text_input(
            "Enter The Required Skills:",
            placeholder="Like: C++,Python,Data Structure",
        )
        # Split the input string into a list of skills
        skills = skill.split(",")

        degree = st.text_input(
            "Enter The Required Degree:", placeholder="Like: B.tech."
        )

    with Data:
        st.header("Data")

    with About:
        st.write("My name is Avdhesh Kumar Yadav and I am developer of this projects")


if __name__ == "__main__":
    main()
