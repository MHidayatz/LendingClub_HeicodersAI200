# Core Packages
import streamlit as st
import streamlit.components.v1 as stc
from streamlit_option_menu import option_menu

# Import our mini apps
from eda_app import run_eda_app
from ml_app import run_ml_app

html_temp = """
		<div style="background-color:#3872fb;padding:10px;border-radius:10px">
		<h1 style="color:white;text-align:center;">Early Stage DM Risk Data App </h1>
		<h4 style="color:white;text-align:center;">Diabetes </h4>
		</div>
		"""

# Use local CSS file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("Style/style.css")

def main():
    st.title("Heicoders AI200: Applied Machine Learning")

    menu = ["Home","EDA","ML","About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Lending Club Defaulters Prediction")

        st. write("""#### 📑 Business Scenario""")
        st.write("""
> You work for the `LendingClub` company which specialises in lending various types of loans to urban customers. When the company receives a loan application, the company has to make a decision for loan approval based on the applicant’s profile. Two types of risks are associated with the bank’s decision:
> - If the applicant is likely to repay the loan, then not approving the loan results in a loss of business to the company
> - If the applicant is not likely to repay the loan, i.e. he/she is likely to default, then approving the loan may lead to a financial loss for the company

> The data given contains the information about past loan applicants and whether they ‘defaulted’ or not. The aim is to identify patterns which indicate if a person is likely to default, which may be used for taking actions such as denying the loan, reducing the amount of loan, lending (to risky applicants) at a higher interest rate, etc.

> When a person applies for a loan, there are two types of decisions that could be taken by the company:
> 1. `Loan accepted`: If the company approves the loan, there are 3 possible scenarios described below:
> - `Fully paid`: Applicant has fully paid the loan (the principal and the interest rate)
> - `Current`: Applicant is in the process of paying the instalments, i.e. the tenure of the loan is not yet completed. These candidates are excluded from the dataset.
> - `Charged-off`: Applicant has not paid the instalments in due time for a long period of time, i.e. he/she has defaulted on the loan

> 2. `Loan rejected`git a: The company had rejected the loan (because the candidate does not meet their requirements etc.). Since the loan was rejected, there is no transactional history of those applicants with the company and so this data is not available within the company nor this dataset.
			""")
        
        st. write("""#### 🎯 Project Objectives""")
        st.write("""
> This In-Class Prediction Challenge is modelled after the `LendingClub Issued Loans` dataset. LendingClub is a US peer-to-peer lending company, headquartered in San Francisco, California. It was the first peer-to-peer lender to register its offerings as securities with the Securities and Exchange Commission (SEC), and to offer loan trading on a secondary market. LendingClub is the world's largest peer-to-peer lending platform.

> Solving this case study will give us an idea about how real business problems are solved using EDA and Machine Learning. In this case study, we will also develop an understanding of risk analytics in banking and financial services and understand how data is used to minimise the risk of losing money while lending to customers.

> In this competition, you'll be parsing through LendingClub’s complete loan dataset and build a machine learning model to predict which of the loans are likely to be defaulted. Loan defaults is an expensive problem which any financial institute that engages in borrowing inadvertently faces. Each year, the financial industry loses billions of dollars due to loan defaults.
        """)


        st.write("""
			#### 💾 Datasource
				- https://archive.ics.uci.edu/ml/datasets/Early+stage+diabetes+risk+prediction+dataset.
			#### App Content
				- EDA Section: Exploratory Data Analysis of Data
				- ML Section: ML Predictor App

			""")
    elif choice == "EDA":
        run_eda_app()
    elif choice == "ML":
        run_ml_app()
    else:
        st.subheader("About")
        st.header(":mailbox: Get In Touch With Me!")
        
        contact_form = """
        <form action="https://formsubmit.co/m.hidayatz86@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your Email" required>
        <textarea name="message" placeholder="Your message here"></textarea>
        <button type="submit">Send</button>
        </form>
        """
        st.markdown(contact_form, unsafe_allow_html=True)
        st.write("Created with [Form Submit](https://formsubmit.co/)")

if __name__ == '__main__':
    main()