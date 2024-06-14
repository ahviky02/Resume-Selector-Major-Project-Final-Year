import streamlit as st #frontend self server
import pickle
from function import *
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

from pytube import YouTube
import pygame
import tempfile
import os
from pydub import AudioSegment


category_mapping = {
    111: None,
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

        # Define keys for the dictionary
        keys = ["Email", "MobileNo.", "Degree", "Skills", "Job Position"]

        # Initialize the dictionary with keys and empty lists as default values
        my_dict = {key: [] for key in keys}

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

                my_dict["Email"].append(Email)
                my_dict["MobileNo."].append(mobile_numbers)
                my_dict["Degree"].append(Degree)
                my_dict["Skills"].append(Skills)
                my_dict["Job Position"].append(category_name)
        df = pd.DataFrame(my_dict)

    with Requirements:
        st.markdown("<h4>Fill Requirements </h4>", unsafe_allow_html=True)
        job_position = st.selectbox(
            "Select Job Position", options=list(category_mapping.values())
        )
        skill = st.text_input(
            "Enter The Required Skills: *Dont forget to saperate with ,*",
            placeholder="Like: C++,Python,Data Structure",
        )

        # Split the input string into a list of skills
        skills = skill.replace(" ", "").split(",")

        degree = st.text_input(
            "Enter The Required Degree:", placeholder="Like: B.Tech."
        )

        if not (df.empty):
            df["Degree Status"] = df["Degree"].apply(
                lambda x: (
                    True
                    if str(x).lower().replace("'", "").replace("{", "").replace("}", "")
                    == degree.lower()
                    else False
                )
            )

            l = list()
            for i in df["Skills"]:
                q = 0
                for j in i:
                    for k in skills:
                        if str(j).lower() == str(k).lower():
                            q += 1
                l.append(q)
            df["Skills status"] = l

            df["Position status"] = df["Job Position"].apply(
                lambda x: (True if x == job_position else False)
            )

            # positon  = 10% , Skills = 55%, Others 15% , degree = 20%
            # ability check
            # percent = 0
            per = list()
            per.clear()
            if job_position is not None:
                if degree is not "":
                    if skill is not "":
                        for index, row in df.iterrows():
                            # 'index' will contain the index of the row
                            # 'row' will contain the data of the row as a pandas Series object
                            if row["Position status"] is True:
                                if row["Degree Status"] is True:
                                    if row["Skills status"] > 0:
                                        percent = (
                                            0.10
                                            + 0.15
                                            + 0.20
                                            + (row["Skills status"] / len(skills))
                                            * 0.55
                                        )
                                        per.append(percent * 100)
                                    else:
                                        percent = 0.10 + 0.15 + 0.20
                                        per.append(percent * 100)
                                else:
                                    if row["Skills status"] > 0:
                                        percent = (
                                            0.10
                                            + 0.15
                                            + (row["Skills status"] / len(skills))
                                            * 0.55
                                        )
                                        per.append(percent * 100)
                                    else:
                                        percent = 0.10 + 0.15
                                        per.append(percent * 100)
                            else:
                                if row["Degree Status"] is True:
                                    if row["Skills status"] > 0:
                                        percent = (
                                            0.15
                                            + 0.20
                                            + (row["Skills status"] / len(skills))
                                            * 0.55
                                        )
                                        per.append(percent * 100)
                                    else:
                                        percent = 0.15 + 0.20
                                        per.append(percent * 100)
                                else:
                                    if row["Skills status"] > 0:
                                        percent = (
                                            0.15
                                            + (row["Skills status"] / len(skills))
                                            * 0.55
                                        )
                                        per.append(percent * 100)
                                    else:
                                        percent = 0.15
                                        per.append(percent * 100)
                                        percent = 0

                    else:
                        for index, row in df.iterrows():
                            if row["Position status"] is True:
                                if row["Degree Status"] is True:
                                    percent = 0.10 + 0.15 + 0.20 + 0.55
                                    per.append(percent * 100)
                                else:
                                    percent = 0.10 + 0.15 + 0.55
                                    per.append(percent * 100)
                            else:
                                if row["Degree Status"] is True:
                                    percent = 0.15 + 0.20 + 0.55
                                    per.append(percent * 100)
                                else:
                                    percent = 0.15 + 0.55
                                    per.append(percent * 100)
                else:
                    if skill is not "":
                        for index, row in df.iterrows():
                            if row["Position status"] is True:
                                if row["Skills status"] > 0:
                                    percent = (
                                        0.10
                                        + 0.15
                                        + 0.20
                                        + (row["Skills status"] / len(skills)) * 0.55
                                    )
                                    per.append(percent * 100)
                                else:
                                    percent = 0.10 + 0.15 + 0.20
                                    per.append(percent * 100)
                            else:
                                if row["Skills status"] > 0:
                                    percent = (
                                        0.15
                                        + 0.20
                                        + (row["Skills status"] / len(skills)) * 0.55
                                    )
                                    per.append(percent * 100)
                                else:
                                    percent = 0.15 + 0.20
                                    per.append(percent * 100)
                    else:
                        for index, row in df.iterrows():
                            if row["Position status"] is True:
                                percent = 0.10 + 0.15 + 0.20 + 0.55
                                per.append(percent * 100)
                            else:
                                percent = 0.15 + 0.20 + 0.55
                                per.append(percent * 100)
            # Job posision no have
            else:
                if degree is not "":
                    if skill is not "":
                        for index, row in df.iterrows():
                            # 'index' will contain the index of the row
                            # 'row' will contain the data of the row as a pandas Series object
                            if row["Degree Status"] is True:
                                if row["Skills status"] > 0:
                                    percent = (
                                        0.10
                                        + 0.15
                                        + 0.20
                                        + (row["Skills status"] / len(skills)) * 0.55
                                    )
                                    per.append(percent * 100)
                                else:
                                    percent = 0.10 + 0.15 + 0.20
                                    per.append(percent * 100)
                            else:
                                if row["Skills status"] > 0:
                                    percent = (
                                        0.10
                                        + 0.15
                                        + (row["Skills status"] / len(skills)) * 0.55
                                    )
                                    per.append(percent * 100)
                                else:
                                    percent = 0.10 + 0.15
                                    per.append(percent * 100)
                    else:
                        for index, row in df.iterrows():
                            # 'index' will contain the index of the row
                            # 'row' will contain the data of the row as a pandas Series object
                            if row["Degree Status"] is True:
                                percent = 0.10 + 0.15 + 0.20 + 0.55
                                per.append(percent * 100)
                            else:
                                percent = 0.10 + 0.15 + 0.55
                                per.append(percent * 100)
                else:
                    if skill is not "":
                        for index, row in df.iterrows():
                            if row["Skills status"] > 0:
                                percent = (
                                    0.10
                                    + 0.15
                                    + 0.20
                                    + (row["Skills status"] / len(skills)) * 0.55
                                )
                                per.append(percent * 100)
                            else:
                                percent = 0.10 + 0.15 + 0.20
                                per.append(percent * 100)
                    else:
                        percent = 0.10 + 0.15 + 0.20 + 0.55
                        per.append(percent * 100)

            # df["Perfomance"] = per
            if job_position is not None or degree != "" or skill != "":
                # st.write(per)
                df_raw = pd.DataFrame(
                    {
                        "Email": df["Email"],
                        "MobileNo.": df["MobileNo."],
                        "Performance": per,
                    }
                )

                # Display the DataFrame using Streamlit
                st.write(df_raw)

    with Data:
        st.header("Data")
        if not df.empty:
            st.write(df[["Email", "MobileNo.", "Skills", "Degree", "Job Position"]])

    with About:
        st.write("  1.Filter the good resume and find the good resume. \n \n 2.  Upload a resume and evaluate its alignment with the requirements of a good resume.\n 3. Upload multiple files at a time.\n 4. Resume Related insights find and download it .csv formats")


if __name__ == "__main__":
    main()