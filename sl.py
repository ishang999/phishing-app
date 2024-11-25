import streamlit as st
import pickle
import numpy as np
import pandas as pd

from urllib.parse import urlparse
import socket

import os
print("Current Working Directory:", os.getcwd())

current_dir = os.path.dirname(os.path.realpath(__file__))
model_path = os.path.join(current_dir, 'model_code/svm_classification_model.pkl')

with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)

scaler_path = os.path.join(current_dir, 'model_code/scaler.pkl')

with open(scaler_path, 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)


#input_url = 'https://www.saffronart.com'
#input_is_bank = 0
#input_asking_for_pay = 1
#input_is_crypto = 0


def main():
    html_temp = """
    <div style="background-color:#0b5394 ;padding:20px">
    <h2 style="color:white;text-align:center;">URL Phishing Prediction </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    input_url = st.text_input("Enter the URL Here","Type Here")
    input_is_bank = st.checkbox("Is the website a bank? (check if true)")
    input_asking_for_pay = st.checkbox("Is the website asking for a payment? (check if true)")
    input_is_crypto = st.checkbox("Is the website asking for cryptocurrency? (check if true)")
    
    safe_html="""  
      <div style="background-color:#38761d;padding:10px >
       <h2 style="color:white;text-align:center;"> This Website is SAFE</h2>
       </div>
    """
    scam_html="""  
      <div style="background-color:#990000;padding:10px >
       <h2 style="color:black ;text-align:center;"> This Website is NOT SAFE</h2>
       </div>
    """

    calc_URLLength = len(input_url) - 1

    parsed_url = urlparse(input_url)
    calc_DomainLength = len(parsed_url.netloc)

    calc_isDomainIP = 0
    try:
        socket.inet_pton(socket.AF_INET, parsed_url.netloc)
        calc_isDomainIP = 1
    except socket.error:
        try:
                socket.inet_pton(socket.AF_INET6, parsed_url.netloc)
                calc_isDomainIP = 1
        except socket.error:
            calc_isDomainIP = 0 
        

    parsed_url_inparts = parsed_url.netloc.split('.')
    calc_TLDLength = len(parsed_url_inparts[-1])

    calc_NoOfSubDomain = len(parsed_url_inparts) - 2

    i = 0
    calc_NoOfObfuscatedChar = 0
    calc_HasObfuscation = 0
    while i < len(input_url):
        if(input_url[i] == '%'):
             if((input_url[i+1] in '0123456789ABCDEFabcdef') and (input_url[i+2] in '0123456789ABCDEFabcdef')):
                 calc_NoOfObfuscatedChar += 3
                 calc_HasObfuscation = 1
        i += 1
    calc_ObfuscationRatio = calc_NoOfObfuscatedChar/calc_URLLength


    modifed_string = parsed_url.netloc.replace("www", "")

    i = 0
    calc_NoOfLettersInURL = 0
    calc_NoOfDegitsInURL = 0
    calc_NoOfEqualsInURL = 0
    calc_NoOfQMarkInURL = 0
    calc_NoOfAmpersandInURL = 0
    calc_NoOfOtherSpecialCharsInURL = 0

    while i < len(modifed_string):
        if (modifed_string[i].isalpha()):
           calc_NoOfLettersInURL += 1  
        elif (modifed_string[i].isdigit()):
            calc_NoOfDegitsInURL += 1  
        elif (modifed_string[i] == "="):
            calc_NoOfEqualsInURL += 1
        elif (modifed_string[i] == "?"):
            calc_NoOfQMarkInURL += 1
        elif (modifed_string[i] == "&"):
            calc_NoOfAmpersandInURL += 1
        else:
            calc_NoOfOtherSpecialCharsInURL += 1
        i += 1
    
    calc_NoOfLettersInURL = calc_NoOfLettersInURL - calc_NoOfSubDomain 
    calc_LetterRatioInURL = calc_NoOfLettersInURL / calc_URLLength
    calc_DegitRatioInURL = calc_NoOfDegitsInURL / calc_URLLength
    calc_NoOfOtherSpecialCharsInURL = calc_NoOfOtherSpecialCharsInURL - 1
    calc_SpacialCharRatioInURL = calc_NoOfOtherSpecialCharsInURL / calc_URLLength

    calc_IsHTTPS = 0
    if (input_url[:8] == "https://"):
        calc_IsHTTPS = 1

    feature_names = [
        'URLLength', 
        'DomainLength', 
        'IsDomainIP', 
        'TLDLength', 
        'NoOfSubDomain',
        'HasObfuscation', 
        'NoOfObfuscatedChar', 
        'ObfuscationRatio', 
        'LetterRatioInURL',
        'NoOfDegitsInURL', 
        'DegitRatioInURL', 
        'NoOfEqualsInURL', 
        'NoOfQMarkInURL',
        'NoOfAmpersandInURL', 
        'NoOfOtherSpecialCharsInURL', 
        'SpacialCharRatioInURL',
        'IsHTTPS', 
        'Bank', 
        'Pay', 
        'Crypto'
    ]

    query_data = np.array([
         calc_URLLength,
        calc_DomainLength,
        calc_isDomainIP,
        calc_TLDLength,
        calc_NoOfSubDomain,
        calc_HasObfuscation,
        calc_NoOfObfuscatedChar,
        calc_ObfuscationRatio,
        calc_LetterRatioInURL,
        calc_NoOfDegitsInURL,
        calc_DegitRatioInURL,
        calc_NoOfEqualsInURL,
        calc_NoOfQMarkInURL,
        calc_NoOfAmpersandInURL,
        calc_NoOfOtherSpecialCharsInURL,
        calc_SpacialCharRatioInURL,
        calc_IsHTTPS,
        input_is_bank,
        input_asking_for_pay,
        input_is_crypto
    ]).reshape(1, -1) 

    query_data_converted = pd.DataFrame(query_data, columns=feature_names)

    scaled_query_data = scaler.transform(query_data_converted)
    prediction = model.predict(scaled_query_data)

    if st.button("Predict Result"):
       
        st.success('The prediction is {}'.format(prediction))

        if prediction == 0:
            st.markdown(scam_html,unsafe_allow_html=True)
        else:
            st.markdown(safe_html,unsafe_allow_html=True)

if __name__=='__main__':
    main()
