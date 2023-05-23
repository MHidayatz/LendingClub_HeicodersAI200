# Core Packages
import streamlit as st

# Load EDA packages
import pandas as pd
import numpy as np

# Load Data vis
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load ML packages
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

import warnings
warnings.filterwarnings("ignore")

# Function to Load data
@st.cache_data #to make it load faster
def load_data(data):
    df = pd.read_csv(data)
    return df

def run_eda_app():
    st.write("EDA - Exploratory Data Analysis - Descriptive")
    #df = pd.read_csv("data/lc_trainingset.csv")
    df = load_data("data/lc_trainingset.csv")
    

    # Create submenu
    submenu = st.sidebar.selectbox("Submenu", ["Descriptive", "Plots","Data Cleaning"] )
    # Descriptive Summary
    if submenu == "Descriptive":
        with st.expander("Dataframe"):
            st.dataframe(df)
        with st.expander("Data Rows/Columns"):
            st.dataframe(df.shape)
        with st.expander("Data Types"):
            st.dataframe(df.dtypes)
        with st.expander("Descriptive Summary"):
            st.dataframe(df.describe().T)
        with st.expander("Missing Value summary"):
            cols = df.columns.to_list()
            st.write('Missing Values in these columns:')
            for col in cols:
                if len(df[df[col].isnull() == True]) != 0:
                     st.write(col, "-",  df[col].isnull().sum())
                else:
                    pass
        with st.expander("Class Distribution"):
            st.dataframe(df['loan_status'].value_counts())

    
    elif submenu == "Data Cleaning":
        st.subheader("Data Cleaning")   
        # Apply funnction to convert Loan status to 1 and 0
        def change_loan_status(loan_status):
            if loan_status in ['Fully Paid', 'Charged Off']:
                return 0
            else:
                return 1
        # Apply the function
        with st.expander("Convert loan status to numerical column"):
            df['loan_status'] = df['loan_status'].apply(change_loan_status)
            st.dataframe(df)

        # Treat missing values
        df['revol_util'] = df['revol_util'].fillna(df['revol_util'].median())
        df['mort_acc'] = df['mort_acc'].fillna(df['mort_acc'].median())
        df['pub_rec_bankruptcies'] = df['pub_rec_bankruptcies'].fillna(df['pub_rec_bankruptcies'].median())
    
        with st.expander("Treating term column"):
            st.write('Before')
            st.dataframe(df['term'].unique())
            df['term'] = df['term'].str.strip().str[:2]
            st.write('After')
            st.dataframe(df['term'].unique())

        # Label Encoding
        with st.expander("Treating sub_grade with label encoding"):
            df = df.sort_values(['sub_grade'])
            st.write('Before label encoding')
            st.dataframe(df['sub_grade'].unique())
            labelencoder = LabelEncoder()
            df['sub_grade'] = labelencoder.fit_transform(df['sub_grade'])
            st.write('After label encoding')
            st.dataframe(df['sub_grade'].unique())
            st.write('sub_grade is the subset of grade, hence sub_grade to be kept and discard grade which may cause multicollinearity')

        # Date Extraction
        with st.expander("Treating Date from Year_cr_line"):
            df['Year_Issued'] = pd.to_datetime(df['issue_d'], format = '%b-%Y').dt.year
            st.dataframe(df['Year_Issued'].value_counts())

            df['Year_cr_line'] = pd.to_datetime(df['earliest_cr_line'], format = '%b-%Y').dt.year
            st.dataframe(df['Year_cr_line'].value_counts())

        # Converting address to postal code
        with st.expander("Converting address to postal code"):
            df['postalcode'] = df['address'].str.split(" ").str[-1]
            st.dataframe(df[['address', 'postalcode']])

        # Dropping of Unnecessary Categorical Features
        with st.expander("Dropping of Unnecessary Categorical Features"):
            pseudo_df = df.drop(['id', 'grade', 'emp_title', 'emp_length', 'initial_list_status', 'address', 'title',
                            'Year_Issued', 'earliest_cr_line','issue_d'], axis =1)
            st.dataframe(pseudo_df.select_dtypes('object').columns)

        # One Hot Encoding
        with st.expander("One Hot Encoding"):
            dummies = pseudo_df.select_dtypes('object').columns.tolist()
            #dummies.remove('loan_status') # have to do on separate row, cant put concurrently abv. remove mutates the list in-place
            st.dataframe(dummies)

            df['verification_status'] = np.where(df['verification_status'] == 'Source Verified', 'Verified', df['verification_status'])
            df['home_ownership'].replace(['NONE', 'ANY'], 'OTHER', inplace = True)

            df['home_ownership'] = df['home_ownership'].str.title()
            df['application_type'] = df['application_type'].str.title()

            for i in dummies:
                df[i] = df[i].str.title()
                st.dataframe(df[i].unique())

            df = pd.get_dummies(df, columns = dummies, drop_first = True)
            st.dataframe(df)



    elif submenu == "Plots":
        st.write("EDA - Exploratory Data Analysis - Plots")
        with st.expander("Distribution of Loan Status Class"):
            fig = px.bar(df['loan_status'].value_counts(), width=800, height=500)
            st.plotly_chart(fig)
            st.write(df['loan_status'].value_counts())

        with st.expander("Distribution of Loan Status with Correlated Variables"):
            fig = px.scatter(df, 
                            x='installment', 
                            y='loan_amnt', 
                            color='loan_status', 
                            template='simple_white')
            st.plotly_chart(fig)
            st.write('It is not easy to tell from the scatter plot as the dataset is unbalanced, having more records which have either fully paid their loan.')
          

        with st.expander("Distribution of Total_acc & Open_ac"):
            df['loan_status'] = df['loan_status'].apply(str)
            trace1 = px.histogram(df, 
                                x = 'total_acc', 
                                color = 'loan_status',  
                                height = 300, width = 500)
            trace2 = px.histogram(df, 
                                x = 'open_acc', 
                                color = 'loan_status', 
                                height = 300, width = 500)

            st.plotly_chart(trace1)
            st.plotly_chart(trace2)
            st.write('Similar frequency distribution between the 2 variables, hence they can be considered as dependent variables. However, both loan status peak around the same value for each variables, hence may not serve as good features.')

        with st.expander("Distribution of Pub_rec_bankruptcies and Pub_rec"):
            df['loan_status'] = df['loan_status'].apply(str)
            trace1 = px.histogram(df, 
                                  x = 'pub_rec_bankruptcies', 
                                  color = 'loan_status',  
                                  height = 500, width = 700)
            trace2 = px.histogram(df, 
                                  x = 'pub_rec', 
                                  color = 'loan_status', 
                                  height = 500, width = 700)
            st.plotly_chart(trace1)
            st.plotly_chart(trace2)

        with st.expander("Corelation Matrix"):
            drop_column = df.copy()
            drop_column = df.drop(['id', 'grade', 'term','sub_grade', 'home_ownership', 'verification_status', 'emp_title', 'emp_length', 'initial_list_status', 'address', 'title',
                            'purpose','application_type','loan_status','earliest_cr_line','issue_d'], axis =1)
            corr = drop_column.corr().round(3)
            fig = px.imshow(corr, 
                             color_continuous_scale = 'plasma', 
                             text_auto = True, aspect = 'auto')
            st.plotly_chart(fig)
            st.write('From the heat map, we can deduce strong positive correlation (>=0.5) between different variables:')
            st.write('* loan_amt ↔ installment')
            st.write('* total_acc ↔ open_acc')
            st.write('* pub_rec ↔ pub_rec_bankruptcies')
            st.write('There is an absence of strong negative correlation between variables')