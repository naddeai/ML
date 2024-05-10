import streamlit as st
import json
import pickle
import pandas as pd

with open('src/options.json', 'r') as f:
    options = json.load(f)

with st.sidebar.form(key='form'):
    
    name = st.text_input('Name')
    
    form_data = {
        'Industry': st.selectbox('Industry', options['Industry']),
        'Ethnicity': st.selectbox('Ethnicity', options['Ethnicity']),
        'Gender': st.selectbox('Gender', options['Gender']),
        'Age': st.slider('Age', 18, 65, 25),
        'CivilStatus': st.selectbox('Civil Status', options['CivilStatus']),
        'YearsEmployed': st.slider('Years Employed', 0, 50, 5),
        'Income': st.slider('Income', 0, 100000, 5000),
    }
    
    button = st.form_submit_button('Submit')
        
    
if button:
    
    st.write('Based on the information you provided:')
    df_input = pd.DataFrame(form_data, index=[name])
    df_input

    with st.spinner('Calculating...'):
        
        with open('src/model.pkl', 'rb') as f:
            model = pickle.load(f)

        probs = model.predict_proba(df_input)
        prob = probs[0][1] * 100
        
        message_base = 'Your approval probability for a credit card is '
        prob_str = f'{prob:.2f}%'
        
        if prob > 50:
            message = message_base + f':green[{prob_str}]'
            st.write(message)
            st.toast('Congratulations! You are approved for a credit card!', icon='🎉')
            st.balloons()
        else:
            message = message_base + f':red[{prob_str}]'
            st.write(message)
            st.toast('Sorry! You are not approved for a credit card.', icon='😢')