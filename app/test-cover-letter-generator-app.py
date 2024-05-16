import google.generativeai as genai
import streamlit as st
import requests
from openai import OpenAI

# Your OpenAI API key (replace with your actual key)
OPENAI_API_KEY = ""

# Setup Gemini API key
gemini_api_key = ''

client = OpenAI(api_key=OPENAI_API_KEY)


# Function to generate a response using OpenAI
def generate_response(prompt):
    try:
        # Call OpenAI API to generate the response
        response = OpenAI.Completion.create(
            model="text-davinci-003",  # Updated to use the latest model
            prompt=prompt,
            max_tokens=150,  # Adjust as needed
            temperature=0.7,  # Adjust for creativity vs. accuracy
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"Error generating response: {e}")
        return None

# Function to send the response to Gemini for refinement
def send_order_to_Gemini(response: str) -> str:
    try:
        # Initialize the Gemini API (configure your API key as shown in the search results)
        genai.configure(api_key=gemini_api_key)
        gemini_base_url = 'https://api.gemini.com/v1/order/new'
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {gemini_api_key}"
        }
        data = {
            "request": "/v1/order/new",
            "response": response
        }

        # Process the response using Gemini
        refined_response = requests.post(gemini_base_url, headers=headers, json=data)
        return refined_response.json().get("refined_response", "Refinement failed")
    except Exception as e:
        print(f"Error refining response with Gemini: {e}")
        return None

# Function to generate a cover letter
def generate_cover_letter(company_name, position_name, resume, job_posting, tone):
    
    prompt = f"I am a job seeker and I need your help to generate a cover letter. Here are the company name: {company_name}, the position title: {position_name}, my resume: {resume}, job description: {job_posting}, the tone of my cover letter: {tone}."
    
    # Call to the ChatGPT model 
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI trained to help write impressive cover letters."},
            {"role": "user", "content": prompt}
        ]
    )
    # except Exception as e:
    #     print(f"Error generating cover letter: {e}")
    return response.choices[0].message.content

# Streamlit user interface setup
def main():
    st.title("Cover Letter Generator")

    with st.form("my_form"):    
        company_name = st.text_input("Enter company name")
        position_name = st.text_input("Enter position title")
        resume = st.text_area("Paste your resume here")
        job_posting = st.text_area("Paste the job posting here")
        tone = st.text_input("Choose the tone (e.g., creative, persuasive, straightforward)")
        submit_button = st.form_submit_button(label='Generate Cover Letter')

    if submit_button and resume and job_posting and position_name:
        cover_letter = generate_cover_letter(company_name, position_name, resume, job_posting, tone)
        if cover_letter:
            st.text_area("Generated Cover Letter", value=cover_letter, height=300)
        else:
            st.error("Failed to generate cover letter.")

if __name__ == "__main__":
    main()