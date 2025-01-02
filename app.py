import streamlit as st
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler,LabelEncoder,OneHotEncoder
import pandas as pd
import pickle


#LOAD THE TRAINED MODEL
model =tf.keras.models.load_model('model.h5')

#LOAD THE ENCODERS AND DECODERS
with open('one_hot_encoder_place.pkl','rb') as file:
    one_hot_encoder_place=pickle.load(file)
with open('label_encoder_gender.pkl','rb') as file:
    label_encoder_gender=pickle.load(file)
with open('scaler.pkl','rb') as file:
    scaler=pickle.load(file)        



#Stream lit app
st.title('Customer Churn Prediction')

geography=st.selectbox('Geography',one_hot_encoder_place.categories_[0])
gender = st.selectbox('Gender', label_encoder_gender.classes_)
age=st.slider('Age',18,92)
balance=st.number_input('Balance')
credit_score=st.number_input('Credit Score')
estimated_salary=st.number_input('Estimated Salary')
tenure=st.slider('Tenure',0,10)
num_of_products=st.slider('Number Of products',1,4)
has_cr_card=st.selectbox('Has Credit card',[0,1])
is_active_member=st.selectbox('Is Active Member',[0,1])




#prepare the input data
input_data=pd.DataFrame({
    'CreditScore':[credit_score],
    'Gender':[label_encoder_gender.transform([gender])],
    'Age':[age],
    'Tenure':[tenure],
    'Balance':[balance],
    'NumOfProducts':[num_of_products],
    'HasCrCard':[has_cr_card],
    'IsActiveMember':[is_active_member],
    'EstimatedSalary':[estimated_salary]

})

#One HOT encoding for geography

geo_encoded=one_hot_encoder_place.transform([[geography]]).toarray()
geo_encoded_df=pd.DataFrame(geo_encoded,columns=one_hot_encoder_place.get_feature_names_out(['Geography']))


#COMBINE THEM
input_data=pd.concat([input_data.reset_index(drop=True),geo_encoded_df],axis=1)

#Scale
input_data_scaled=scaler.transform(input_data)

#Predict Churn

prediction=model.predict(input_data_scaled)
prediction_proba=prediction[0][0]

if prediction_proba>0.5:
    st.write("Customer is likely to Churn.")
else:
    st.write("Customer is not likely to Churn.")    



