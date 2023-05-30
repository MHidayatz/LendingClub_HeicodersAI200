# Core Packages
import streamlit as st
import streamlit.components.v1 as stc
from streamlit_option_menu import option_menu

#Load ML Packages
import joblib
import os
import numpy as np
import sklearn as sk
import xgboost as xgb

attrib_info = """
#### Attribute Information:
    - Age 1.20-65
    - Sex 1. Male, 2.Female
    - Polyuria 1.Yes, 2.No.
    - Polydipsia 1.Yes, 2.No.
    - sudden weight loss 1.Yes, 2.No.
    - weakness 1.Yes, 2.No.
    - Polyphagia 1.Yes, 2.No.
    - Genital thrush 1.Yes, 2.No.
    - visual blurring 1.Yes, 2.No.
    - Itching 1.Yes, 2.No.
    - Irritability 1.Yes, 2.No.
    - delayed healing 1.Yes, 2.No.
    - partial paresis 1.Yes, 2.No.
    - muscle stiness 1.Yes, 2.No.
    - Alopecia 1.Yes, 2.No.
    - Obesity 1.Yes, 2.No.
    - Class 1.Positive, 2.Negative.

"""
label_dict = {"No":0,"Yes":1}
term_map = {"36 months":0,"60 months":1}
sub_grade_map = {"A1":0,"A2":1,"A3":2,"A4":3,"A5":4}

['term','sub_grade_map']


# Define functions
def get_fvalue(val):
	feature_dict = {"No":0,"Yes":1}
	for key,value in feature_dict.items():
		if val == key:
			return value 

def get_value(val,my_dict):
	for key,value in my_dict.items():
		if val == key:
			return value 
		
# Load ML Models
@st.cache
def load_model(model_file):
	loaded_model = joblib.load(open(os.path.join(model_file),"rb"))
	return loaded_model

def run_ml_app():
    st.subheader("From ML Section")
    st.info("This is under construction!")

    #Layout
    col1,col2 = st.columns(2)

    with col1:		
        loan_amount = st.number_input("Loan Amount",0,10000)
        term = st.radio("Term",("36 months","60 months"))
        int_rate = st.number_input("Interest Rate",0,31)
        installment = st.number_input("Installment",0,2000)
        sub_grade = st.selectbox("Sub Grade",["A1","A2","A3","A4","A5"]) 

    with st.expander("Your Selected Options"):
        result = {'Loan Amount':loan_amount,
		'term':term,
		'int_rate':int_rate,
		'installment':installment,
		'sub_grade':sub_grade}
	
        st.write(result)
        encoded_result = []
        for i in result.values():
            if type(i) == int:
                encoded_result.append(i)
            elif i in ["36 months","60 months"]:
                res = get_value(i,term_map)
                encoded_result.append(res)
            else:
                encoded_result.append(get_fvalue(i))

        st.write(encoded_result)

		# st.write(encoded_result)
    with st.expander("Prediction Results"):
        single_sample = np.array(encoded_result).reshape(1,-1)
        loaded_model = load_model("XGBoost_SMOTE.pkl")
        prediction = loaded_model.predict(single_sample)
        pred_prob = loaded_model.predict_proba(single_sample)
        st.write(prediction)
        
        if prediction == 1:
            st.warning("Positive Risk-{}".format(prediction[0]))
            pred_probability_score = {"Negative DM":pred_prob[0][0]*100,"Positive DM":pred_prob[0][1]*100}
            st.subheader("Prediction Probability Score")
            st.json(pred_probability_score)
        else:
            st.success("Negative Risk-{}".format(prediction[0]))
            pred_probability_score = {"Negative DM":pred_prob[0][0]*100,"Positive DM":pred_prob[0][1]*100}
            st.subheader("Prediction Probability Score")
            st.json(pred_probability_score)