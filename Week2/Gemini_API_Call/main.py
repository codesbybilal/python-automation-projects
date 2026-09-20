import logging
logging.getLogger().setLevel(logging.ERROR)
from google import genai
from dotenv import load_dotenv
import os, re           #Regex is a module to remove the special characters included with the
                        #response from the API request
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key= api_key)
while True:
    prompt=input("YOU: ")
    if prompt.lower() in ["exit", "quit", "stop"]:
        break
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )
    response = response.text
    response = re.sub(r'\*+', "", response) 
    print("AI: ",response.strip())
