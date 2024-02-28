import streamlit as st
import pickle
import re
import nltk
from function import *

nltk.download("punkt")
nltk.download("stopwords")
# loading models
clf = pickle.load(open("clf.pkl", "rb"))
tfidf = pickle.load(open("tfidf.pkl", "rb"))


# web app
def main():
    st.title("Resume Screening App")
    uploaded_file = st.file_uploader("Choose files", type=["txt", "pdf"])

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
        st.write(prediction_id)

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

        # st.write("### Extracted Text:")
        # st.write(text)

        st.write("Email:", Email)
        st.write("Degree:", Degree)
        st.write("Skills:", Skills)
        # print(mobile_numbers)
        st.write("Mobile Number:", mobile_numbers)
    # ttt = extract_text_from_pdf(uploaded_file)


# python main
if __name__ == "__main__":
    main()
