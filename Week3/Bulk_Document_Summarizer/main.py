#-----------------Importing packages---------------------
from google import genai
from google.genai import types
from dotenv import load_dotenv
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
import logging
from pathlib import Path
import pdfplumber
from pdfminer.pdfparser import PDFSyntaxError
from pdfminer.pdfdocument import PDFPasswordIncorrect
import os
import sys
import json
logging.getLogger().setLevel(logging.ERROR)
#------------------------------------------------------------
load_dotenv()
#---------------------Setting client for API call------------
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    client = genai.Client(api_key=api_key)
else:
    print("No API key is found.")
    sys.exit()
MODEL_NAME = "gemini-3.5-flash-lite"
INPUT_FOLDER_NAME = "input"
OUTPUT_FOLDER_NAME = "output"
EMPTY_PDF_ERROR_MSG = "No text is found in the pdf."
API_FAILURE_ERROR_MSG = "AI failed to generate a response."
JSON_PARSING_ERROR_MSG = "Failed to parse the JSON."
SYSTEM_INSTRUCTION = """
You are an information extraction and document summarization tool.

Given the text extracted from a PDF document, perform these tasks:

1. Summary:
   - Generate a summary consisting of exactly three paragraphs separated by new line characters.
   - Include the main ideas and important details from the source text.
   - Do not introduce information that is not present in the document.

2. Key Topics:
   - Extract the main topics discussed in the document.
   - Return the topics as a list of concise strings.
   - Include only topics supported by the source text.

3. Missing Information:
   - If a requested field cannot be determined from the provided text,
     return Null for that field.
   - Do not invent, assume, or guess information.

Base your response entirely on the provided document text.
"""
input_folder = Path(INPUT_FOLDER_NAME)
output_folder = Path(OUTPUT_FOLDER_NAME)
output_folder.mkdir(parents=True, exist_ok=True)
if not(os.path.exists(input_folder)):
    print(f"The {INPUT_FOLDER_NAME} does not exist in this directory. Generate one")
    sys.exit()
pdf_files = list(input_folder.glob("*.pdf"))
if not pdf_files:
    print(f"No pdf files are present in {input_folder}")
    sys.exit(1)
workbook = Workbook()
worksheet = workbook.active
worksheet.title = "Document Summaries"
worksheet.append(["File Name", "Word Count", "Key Topics", "Summary"])

#-----------------Formatting worksheet--------------------
header_fill = PatternFill(
    fill_type="solid",
    fgColor="D9EAF7"
)

header_font = Font(
    bold=True,
    size=12
)

header_alignment = Alignment(
    horizontal="center",
    vertical="center",
    wrap_text=True
)

for cell in worksheet[1]:
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = header_alignment

worksheet.row_dimensions[1].height = 25
#---------------------------------------------------------
for pdf in pdf_files:
    try:
        with pdfplumber.open(pdf) as pdf_file:
            pages = []
            for page in pdf_file.pages:
                page_text = page.extract_text()
                pages.append(page_text)
            extracted_text = "\n".join(page for page in pages if (page and page.strip()))
            word_count = len(extracted_text.split())
    except PDFSyntaxError:
        print(f"The {pdf.stem} is a corrupted or a renamed text file. Skipping it...")
        continue
    except PDFPasswordIncorrect:
        print(f"The {pdf.stem} file is password protected. Cannot open it. Skipping...")
        continue
    except Exception as e:
        print(f"Something went wrong with opening {pdf.stem} file. {e}. Skipping it...")
        continue
    if extracted_text:
        try:
            response = client.models.generate_content(
                model = MODEL_NAME,
                contents= extracted_text,
                config= types.GenerateContentConfig(
                    system_instruction= SYSTEM_INSTRUCTION,
                    response_mime_type= "application/json",
                    response_schema= {
                        "type":"object",
                        "properties":{
                            "summary_paragraphs": {
                                "type":"string",
                                "nullable": True
                            },
                            "key_topics":{
                                "type":"array",
                                "items":{
                                    "type":"string"
                                },
                                "nullable": True
                            }
                        },
                        "required":["summary_paragraphs", "key_topics"]
                    }
                )
            )
            try:
                ai_extracted_response = json.loads(response.text)
                summary_paragraphs = ai_extracted_response["summary_paragraphs"]
                file_name = pdf.stem
                if summary_paragraphs is not None and summary_paragraphs != "":
                    output_file = output_folder / f"{file_name}_summary.txt"
                    with open(output_file, "w", encoding= "utf-8") as file:
                        file.write(summary_paragraphs)
                else:
                    summary_paragraphs = "Unable to generate summary."
                if ai_extracted_response["key_topics"]:
                    key_topics = ", ".join(ai_extracted_response["key_topics"])
                else:
                    key_topics = "No key topics are found from text."
                worksheet.append([file_name, word_count, key_topics, summary_paragraphs])
            except json.JSONDecodeError:
                print(f"Failed to parse JSON for {pdf}")
                worksheet.append([pdf.stem, word_count, JSON_PARSING_ERROR_MSG, JSON_PARSING_ERROR_MSG])
                continue
        except Exception as e:
            print(f"Something went wrong with response generation of {pdf}")
            worksheet.append([pdf.stem, word_count, API_FAILURE_ERROR_MSG, API_FAILURE_ERROR_MSG])
            continue
    else:
        print(f"No extracted text is found in {pdf}")
        worksheet.append([pdf.stem, word_count, EMPTY_PDF_ERROR_MSG, EMPTY_PDF_ERROR_MSG])
        continue

#-----------------Formatting data rows--------------------
for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row):
    for cell in row:
        cell.alignment = Alignment(
            vertical="top",
            wrap_text=True
        )

# Set column widths
worksheet.column_dimensions["A"].width = 25
worksheet.column_dimensions["B"].width = 15
worksheet.column_dimensions["C"].width = 35
worksheet.column_dimensions["D"].width = 70

# Keep the header visible and enable filtering
worksheet.freeze_panes = "A2"
worksheet.auto_filter.ref = worksheet.dimensions
#---------------------------------------------------------

workbook.save("output/master_report.xlsx")
workbook.close()