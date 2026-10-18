import os
import pdfplumber
import logging
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json,sys
logging.getLogger().setLevel(logging.ERROR)
from datetime import datetime
today = datetime.today().strftime("%Y-%m")

#-------------------------Function Declaration----------------
def merge_intervals(intervals):
    if not intervals:
        return []
    sorted_intervals = sorted(intervals)
    merged_intervals = [sorted_intervals[0]]
    for start, end in sorted_intervals[1:]:
        last_start, last_end = merged_intervals[-1]
        if last_end >= start:
            merged_intervals[-1]= (last_start, max(last_end, end))
        else:
            merged_intervals.append((start, end))
    return merged_intervals
def to_interval(start, end):
    start_year, start_month = start.split("-")
    end_year, end_month = end.split("-")
    start_month_index = (int(start_year))*12 + (int(start_month))
    end_month_index = (int(end_year))*12 + (int(end_month)) +1 #Taking end month index as exclusive
    interval = (start_month_index, end_month_index)
    return interval    
def calculate_total_experience(work_experience):
    intervals = []
    for job in work_experience:
        start_date = job["start_date"]
        end_date = job["end_date"]
        if end_date.lower() == "present":
            end_date = today
        if not(start_date and end_date):
            print(f"No valid job duration found for {job['company']}")
            continue
        try:
            start_date_object = datetime.strptime(start_date,"%Y-%m")
            end_date_object = datetime.strptime(end_date, "%Y-%m")
            if end_date_object >= start_date_object:
                interval = to_interval(start_date, end_date)
                if interval:
                    intervals.append(interval)
        except ValueError:
            print(f"No valid job duration found for {job['company']}")
            continue
    merged_intervals = merge_intervals(intervals)
    total_years = round(((sum((end - start) for start, end in merged_intervals))/12),1)
    if total_years == 0.0:
        return None
    return total_years
#-------------------------------------------------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client= genai.Client(api_key=api_key)
pdf_path = input("Enter the path of the pdf file: ")
if os.path.exists(pdf_path):
    print("The pdf file exists.")
else:
    print("File does not exist at the provided path")
    sys.exit()
extension = os.path.splitext(pdf_path)[1]
if extension.lower()== ".pdf":
    try:
        with pdfplumber.open(pdf_path) as pdf:
            pages = []
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    pages.append(page_text)
            page_text = "\n".join(pages).strip()
    except Exception as e:
        print(f"The text cannot be extracted from the pdf. {e}")
        sys.exit()
else:
    print("Not a pdf file.")
    sys.exit()
if page_text.strip() == "":
    print("No extractable text is found. ")
    sys.exit()
try:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=page_text,
        config=types.GenerateContentConfig(
            system_instruction="You are a very good information extraction tool. You are given the details from the resume of a person, you have to extract name of person, email for contact, phone number, education as array, work experiences as array, skills.Do not invent or guess anything form your side. If any field is empty, then return empty list for that specific field, return empty string for text field and null for number fields. Do not include any false information, and strictly rely on the given data. If some job role has no starting and ending dates, then do not invent it by yourself. ",
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties":{
                    "name":{
                        "type": "string"
                    },
                    "email":{
                        "type":"string"
                    },
                    "phone":{
                        "type":"string"
                    },
                    "education":{
                        "type":"array",
                        "items":{
                            "type":"object",
                            "properties":{
                                "degree":{
                                    "type":"string"
                                },
                                "institution":{
                                    "type":"string"
                                },
                                "start_year":{
                                    "type":"string"
                                },
                                "end_year":{
                                    "type":"string"
                                }
                            },
                        "required":["degree","institution","start_year","end_year"]
                        }
                    },
                    "work_experience":{
                        "type":"array",
                        "items":{
                            "type":"object",
                            "properties":{
                                "job_title":{
                                    "type":"string"
                                },
                                "company":{
                                    "type":"string"
                                },
                                "start_date":{
                                    "type":"string",
                                    "description": "The date strictly formatted as YYYY-MM (e.g., 2020-10)."
                                },
                                "end_date":{
                                    "type":"string",
                                    "description": "The date strictly formatted as YYYY-MM (e.g., 2020-10)."
                                },
                                "description":{
                                    "type":"string"
                                }
                            },
                            "required":["job_title","company","start_date","end_date","description"]
                        }
                    },
                    "skills":{
                        "type":"array",
                        "items":{
                            "type":"string"
                        }
                    }
                },
                "required":["name", "email", "phone", "education", "work_experience", "skills"]

            }
        )
    )
    try:
        extracted_details = json.loads(response.text)
        extracted_details["total_years_experience"] = calculate_total_experience(extracted_details["work_experience"])
        with open("parsed_cv.json","w",encoding= "utf-8") as file:
            json.dump(extracted_details, file, indent=4, ensure_ascii=False)
            print("JSON parsed successfully and stored in 'parsed_cv.json' file.\n")
    except json.JSONDecodeError:
        print("Failed to parse JSON.")
        sys.exit()
except Exception as e:
    print(f"Something went wrong. {e}")

