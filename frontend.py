import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"

st.title("Insurance Premium Prediction")

st.markdown("Enter your details below:")

#Input fields
age = st.number_input("Age", min_value=1, max_value=120, value=30)
weight = st.number_input("Weight (kg)", min_value=1.0, value=70.0)
height = st.number_input("Height (m)", min_value=0.5, max_value=3.0, value=1.75)
income_lpa = st.number_input("Income (Lakhs per annum)", min_value=1.0, value=10.0)
smoker = st.selectbox("Are you a smoker?",options=["Yes", "No"])
city = st.text_input("City", value="Mumbai")
occupation = st.selectbox("Occupation", 
    ["retired", "freelancer", "student", "government_job", "business_owner", "unemployed", "private_job"])  

if st.button("Predict Premium"):
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try: 
        response = requests.post(API_URL, json=input_data)
        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted Insurance Premium: **{result['predicted']}**")
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("Failed to connect to the API. Please ensure the server is running.")