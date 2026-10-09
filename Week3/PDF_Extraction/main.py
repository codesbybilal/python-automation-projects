import logging
logging.getLogger().setLevel(logging.ERROR)
import pdfplumber
from google import genai
from dotenv import load_dotenv
import os, json,sys
from google.genai import types
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
def extractText(filePath):
    pages=[]
    with pdfplumber.open(filePath) as pdf:
        for page in pdf.pages:
            pageText = page.extract_text()
            if pageText:
                pages.append(pageText)
    return "\n".join(pages).strip()

cleaned_text = extractText("./DummyChallan.pdf")
if not cleaned_text:
    print("No text available in uploaded document.")
    sys.exit(1)
with open("extracted.txt", "w", encoding="utf-8") as f:
    f.write(cleaned_text)

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=cleaned_text,
        config=types.GenerateContentConfig(
            system_instruction="You are a very good information extraction tool. The text is given to you and from the text you have to extract the student name, the total payable fee amount and the due date. Extract only these three fields. If there is no data about any of these fields, return an empty string. Return only valid JSON object.",
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": {
                    "student_name":{
                        "type": "string",
                    },
                    "fee_amount": {
                        "type": "string",
                    },
                    "due_date":{
                        "type": "string",
                    }
                },
                "required": ["student_name", "fee_amount", "due_date"]
            }
        )
        
    )
    extractedDetails = json.loads(response.text)
    print(extractedDetails)
except json.JSONDecodeError:
    print("Could not get a valid json object.")
except Exception as e:
    print(f"Something went wrong. {e}")