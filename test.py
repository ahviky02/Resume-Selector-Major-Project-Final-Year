from library import *


def main():
    st.title("Tabbed Layout Example")

    tabs = ["Section 1", "Section 2", "Section 3"]
    selected_tab = st.selectbox("Choose a section:", tabs)

    if selected_tab == "Section 1":
        resume_screening()
    elif selected_tab == "Section 2":
        resume_requirements()


if __name__ == "__main__":
    main()
