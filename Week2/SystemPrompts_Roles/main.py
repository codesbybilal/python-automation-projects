import logging
logging.getLogger().setLevel(logging.ERROR)
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os, re
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
#----------------------Functions Declarations-----------------------
def displaySystemRoles():
    print("This AI agent can behave like a:")
    print("1. A Python Code Reviewer")
    print("2. An Urdu//English translator")
    print("3. A strict grammar corrector")


def inputSystemRole():
    try:
        choice = int(input("Select the behaviour of agent (1,2 or 3): "))
        if choice==1 or choice ==2 or choice ==3:
            return choice
        else:
            print("Invalid Choice. Select only 1,2 or 3.")
            return inputSystemRole()
    except ValueError:
        print("Please enter a number (1, 2 or 3).")
        return inputSystemRole()

def roleOfSystem(choice):
    if choice == 1:
        result="""You are a python code reviewer. Analyze the python code, if it is
        not in python, say The code is not in python language. If there are bugs and errors in 
        the code either syntactically or logically , specify it and also give the corrected version. Also provide any improvement that can be made in the given code. Do not comment on anything outside of bugs, corrections, and functional improvements — no opinions on style or naming unless they cause an issue."""
    elif choice == 2:
        result="""You are a very accurate Urdu to English and English to Urdu translator. If the input is not in any of English or Urdu language, say The input is not in either English or Urdu language. If the input is in Urdu language, translate it into English, if it is in English language, translate it into Urdu. The language Urdu with the script of English often referred to as Roman Urdu as in "Kya haal hai" is considered as an Urdu input and should be translated into English. Be very precise about the contextual meaning of the input language, and translate the text contextually not with literal meanings."""
    elif choice == 3:
        result = """You are a strict English grammar corrector tool. If the input is not in English, say The language must be English. If it is in English language, check strictly for grammar mistakes and then highlight the mistakes , tell why they are considered as a mistake and then give the corrected version. Go through each line and check for spelling or grammar errors. Also consider idioms and other phrases by their contextual meaning."""
    else:
        print("The input is invalid.")
        result = 0
    return result

def responseGenerator(system_instruction, inputPrompt):
    response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=inputPrompt,
    config=types.GenerateContentConfig(
        system_instruction=system_instruction
    )
    )
    response = response.text
    response = re.sub(r'\*+', "", response)
    return response

displaySystemRoles()
choice = inputSystemRole()
system_instruction = roleOfSystem(choice)
inputPrompt= input("Enter the prompt: ")
response = responseGenerator(system_instruction, inputPrompt)
print("AI: ", response)