import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

st.title("Full Year Business Forecast(2025)")
#load data
uploaded_file=st.file_uploader("Upload MIS Data Excel File", type=["xlsx"])
if uploaded_file:
    df=pd.read_excel(uploaded_file,sheet_name="Sheet1")
    df['Reg.Date']=pd.to_datetime(df["Reg.Date"],errors='coerce')
    df['YearMonth']=df['Reg.Date'].dt.to_period('M')
    #st.dataframe(df)
    #filter options
    technologies=df['Subject'].drop().unique()
    colleges=df['College'].dropna().unique()
    location=df['Location'].dropna().unique()
    selected_tech=st.selectbox("Select Technologies",sorted(technologies))
    selected_college=st.selectbox("Select College (Optional)",['All']+sorted(colleges.tolist()))
    selected_location=st.selectbox("Select Location (Optional)",['All']+sorted(location.tolist))
    # apply filter
    data=[df['Subject']==selected_tech]
     #st.dataframe(data)
    if selected_college!='All':
       data=data[data['college']==selected_college]
    if selected_location!='All':
        data=data[data['Location']==selected_location]
    #group by Month
    monthly=data.groupby('YearMonth').size().reset_index(name='SNo.') 
    monthly=monthly.set_index('YearMonth').asfreq('M').fillna(0)
    monthly.index=monthly.index.to_timestamp()
    if len(monthly)>=2:
        #prepare regression model
        x=np.array([d.toordinal() for d in monthly.index]).reshape(-1,1)
        y=monthly['SN0.'].values
        model=LinearRegression()
        model.fit(x,y)
        #predict All months of 2025
        future_dates=pd.date_range(start="2025-01-01",end="2025-12-01",freq='MS')
        x_future=np.array([d.toordinal() for d in monthly.index]).reshape(-1,1)
        y_pred=model.predict(x_future)
        st.dataframe(y_pred)
        #show predicted value
        forecast_df=pd.DataFrame({
            'Month':future_dates.strftime('%B %Y'),
            'predicted Enrollments' :np.round(y_pred).astype(int)
        })
        st.subheader("Monthly prediction of 2025")
        st.dataframe(forecast_df)
        # show total prediction
        st.success(f"Total predicted Enrollments for 2025:{int(np.round(y_pred).sum())}")
    else:
        st.warning("Not enough data for prediction")