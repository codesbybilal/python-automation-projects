import logging
logging.getLogger().setLevel(logging.ERROR)
from google import genai
from dotenv import load_dotenv
from google.genai import types
import os, json
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
#--------------------------Function Declaration------------------
def displayMenu():
    print("""========AI Text Processing Toolkit========
    1. Text Summarizer
    2. Translator
    3. Grammar Fixer
    4. Keyword Extractor
    5. Sentiment Classifier
    6. Exit
    """)

def inputChoice():
    try:
        choice = int(input("Enter your choice (1-6): "))
        if choice >=1 and choice <=6:
            return choice
        else:
            print("Invalid Choice. Select from 1-6.")
            return inputChoice()
    except ValueError:
        print("Please enter a number (1-6).")
        return inputChoice()
def systemRole(choice):
    if choice==1:
        result="""You are a text summarization assistant.
Summarize the user's provided text while preserving its main ideas and important information.
The summary must not exceed the maximum number of words specified by the user.
Do not add information that is not present in the original text.
Return only the summary, without headings, explanations, or quotation marks."""
    elif choice==2:
        result="""You are a translation assistant.
Translate the user's provided text accurately into the language specified by the user.
Preserve the original meaning, tone, and important details.
Do not explain the translation or add additional information.
Return only the translated text."""
    elif choice==3:
        result="""You are a grammar correction assistant.
Correct grammar, spelling, punctuation, and sentence structure in the user's provided text.
Preserve the original meaning and intent.
Improve clarity and naturalness when necessary, but do not add new information.
Return only the corrected and improved text."""
    elif choice==4:
        result="""You are a keyword extraction assistant.
Extract the top N most important and relevant keywords or key phrases from the user's provided text.
Rank them by relevance to the main topic.
Do not include unnecessary common words.
Return exactly N keywords when enough relevant keywords are available.
If fewer than N meaningful keywords exist, return only the meaningful keywords available.
Return the result according to the provided response schema."""
    elif choice==5:
        result="""You are a sentiment analysis assistant.
Analyze the sentiment expressed in the user's provided text.
Classify it as exactly one of: positive, negative, or neutral.
Provide a confidence score between 0 and 1 representing your confidence in the classification.
Base the classification only on the information and sentiment expressed in the provided text.
Return the result according to the provided response schema."""
    return result
def responseGenerator(inputPrompt, system_instruction, schema=None, responseType=None):
    config_arguments={"system_instruction": system_instruction}
    if responseType:
        config_arguments["response_mime_type"]=responseType
        config_arguments["response_schema"]=schema

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=inputPrompt,
        config=types.GenerateContentConfig(**config_arguments)
    )
    return response.text
def textSummarize(text, maxWords):
    system_instruction=systemRole(1)
    response = responseGenerator(f"Text: {text} MaxWordsInOutput: {maxWords}", system_instruction )
    return response
def textTranslate(text, language):
    system_instruction= systemRole(2)
    response = responseGenerator(f"Text: {text} Translate into {language}", system_instruction)
    return response
def fixGrammar(text):
    system_instruction=systemRole(3)
    response = responseGenerator(text, system_instruction)
    return response
def extractKeywords(text, n):
    system_instruction=systemRole(4)
    responseType = "application/json"
    schema = {
        "type":"array",
        "items":{
            "type":"string"
        }
    }
    response = responseGenerator(f"Text: {text} \n Return {n} keywords", system_instruction, schema, responseType)
    extractedDetails = json.loads(response)
    return extractedDetails
def classifySentiment(text):
    system_instruction=systemRole(5)
    responseType="application/json"
    schema={
        "type":"object",
        "properties":{
            "sentiment":{
                "type":"string"
            },
            "confidence":{
                "type":"number"
            }
        },
        "required":["sentiment", "confidence"]
    }
    response = responseGenerator(text, system_instruction, schema, responseType)
    extractedDetails = json.loads(response)
    return extractedDetails
def callFunctions(choice):
    if choice==1:
        text = input("Enter the text to summarize: ")
        maxWords = input("Enter the number of max words in output: ")
        result = textSummarize(text, maxWords)
    elif choice ==2:
        text = input("Enter the text you want to translate: ")
        language = input("Enter the language to translate into: ")
        result = textTranslate(text, language)
    elif choice == 3:
        text= input("Enter the text to fix the grammar: ")
        result = fixGrammar(text)
    elif choice == 4:
        text= input("Enter the text to extract the keywords from: ")
        n = input("Enter the total number of top extracted keywords: ")
        result= extractKeywords(text, n)
    elif choice == 5:
        text= input("Enter the text to classify its sentiment: ")
        result = classifySentiment(text)
    return result
#--------------------------------------------------------------------------------
displayMenu()
choice =inputChoice()
if choice == 6:
    exit()
result = callFunctions(choice)
print("AI: ", result)
