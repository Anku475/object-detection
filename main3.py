import streamlit as st
import pandas as pd
import joblib


#load model and encoders
model=joblib.load('student_performance_model.pkl')
technology_encoder=joblib.load('technology_encoder.pkl')
grade_encoder=joblib.load('grade_encoder.pkl')

st.subheader('student performance analysis and prediction app')
st.write('fill the student score below to predict their final grade')

#user inputs
technology=st.selectbox("Technology",technology_encoder.classes_)
welcome_test=st.slider('welcome Test',30,50,40)
presentation=st.slider('Presentation',90,150,120)
mini_projects=st.slider('Mini projects', 60,100,80)
hrskills=st.slider('HR Skills',90,150,120)
project_presentation=st.slider('Project Presentation',160,250,205)
project_submission=st.slider('Project Submission',200,300,251)
attendence=st.slider('Attendence',70,100,85)
discpline=st.slider('Discipline',60,100,80)