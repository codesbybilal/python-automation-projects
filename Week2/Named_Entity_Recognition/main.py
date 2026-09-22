import logging
logging.getLogger().setLevel(logging.ERROR)
from google import genai
from dotenv import load_dotenv
from google.genai import types
import os, json

#---------------------Function declaration----------------
def displayInfo(dictionary):
    print("Extracted Information: \n")
    print("Persons: ")
    for names in dictionary['persons']:
        print(names)
    print("\nDates: ")
    for dates in dictionary['dates']:
        print(dates)
    print("\nLocations: ")
    for locations in dictionary['locations']:
        print(locations)
    print("\nOrganizations: ")
    for org in dictionary['organizations']:
        print(org)
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
inputPrompt = input("Enter the sentence you want to extract details from: ")
try:
    response = client.models.generate_content(
        model = "gemini-3.5-flash-lite",
        contents= inputPrompt,
        config=types.GenerateContentConfig(
            system_instruction="You are an entity/information extractor AI. Extract persons' names, dates, locations and organizations from input text. Extract exactly these four fields. Each field must be a list. If there is no data about any of the fields return an empty list for that field. Return only the valid JSON object.",
            response_mime_type= "application/json",
            response_schema={
    "type": "object",
    "properties": {
        "persons": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "dates": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "locations": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "organizations": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    },
    "required": ["persons", "dates", "locations", "organizations"]
    
}
        )
    )
    extractedDetails = json.loads(response.text)
    displayInfo(extractedDetails)
except json.JSONDecodeError:
    print("Could not get a valid JSON object.")
except Exception as e:
    print(f"Something went wrong.{e} ")
