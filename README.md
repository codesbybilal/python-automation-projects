# Python Automation Projects

A collection of Python projects built while learning **Python automation, APIs, File I/O, and practical scripting**.

This repository documents my progress through hands-on projects rather than only following tutorials.

---

## 📚 Week 1

### 1. GitHub API Practice

**File:** `Week1/githubAPIcall.py`

A simple Python script that uses the **GitHub REST API** to retrieve information about a GitHub user.

#### Concepts practiced

* REST APIs
* HTTP GET requests
* `requests` library
* JSON responses
* Python dictionaries
* Accessing API data

#### Information retrieved

* GitHub username
* Name
* Bio
* Followers

---

### 2. REST Countries API Practice

**File:** `Week1/pakistanAPIcall.py`

A Python script that uses the **REST Countries API** to retrieve information about a country.

#### Concepts practiced

* API requests
* JSON data
* Nested dictionaries
* Lists inside JSON responses
* Navigating structured API data

#### Information retrieved

* Population
* Capital
* Currency
* Country information

---

### 3. ContactBookCLI

**Folder:**` Week1/ContactBookCLI/`

A command-line contact book built with Python to practice **File I/O** and working with persistent local data without using a database.

Contacts are stored in a local text file.

#### Features

* Add a contact
* Store contact name and phone number
* Search for a contact by name
* Read contacts from a `.txt` file
* Handle contacts using Python file operations

#### Concepts practiced

* `open()`
* Reading files
* Writing files
* File modes such as `r` and `w`
* `with open(...)`
* String processing
* `.strip()`
* Splitting strings
* Functions
* Loops
* Conditional statements
* Command-line interaction

#### Data storage

The project uses a simple text file instead of a database.

Example:

```text
Ali | 03001234567
Ahmed | 03111234567
Usman | 03221234567
```

This project helped me understand how applications can persist data using files before moving to databases.

---

### 4. Automated Weather Report

**Folder:** `Week1/Automated Weather Report/`

A Python automation script that reads a list of cities from a text file, retrieves their current weather information from the **OpenWeatherMap API**, and generates a formatted weather report.

#### Workflow

```text
cities.txt
    ↓
Python reads cities
    ↓
OpenWeatherMap API
    ↓
JSON response
    ↓
Extract weather data
    ↓
Generate report
    ↓
weather_report.txt
```

#### Features

* Reads cities from `cities.txt`
* Fetches weather data through an API
* Retrieves temperature
* Retrieves humidity
* Retrieves weather description
* Handles unsuccessful API requests
* Generates a timestamp
* Creates a formatted weather report
* Uses environment variables to protect the API key

#### Concepts practiced

* Python File I/O
* REST APIs
* `requests`
* JSON
* API status codes
* Environment variables
* `.env`
* `python-dotenv`
* `datetime`
* Functions
* Loops
* Error handling

---

## 🛠️ Technologies & Concepts

* Python
* REST APIs
* JSON
* `requests`
* `python-dotenv`
* File I/O
* Environment variables
* Command-line applications
* Git
* GitHub

---

## 🔐 Security

Sensitive information such as API keys is stored in a `.env` file and excluded from Git using `.gitignore`.

The virtual environment and generated weather report are also excluded from version control.

---

## 🎯 Purpose

The purpose of this repository is to build practical Python skills through progressively more useful projects.

The learning path focuses on understanding **how and why the code works**, rather than simply copying solutions.

---

## 📈 Progress

### Week 1 — Python Automation Foundations

* [x] Python File I/O
* [x] Contact Book CLI
* [x] REST APIs
* [x] GitHub API
* [x] REST Countries API
* [x] Weather API
* [x] JSON data navigation
* [x] Environment variables
* [x] `.gitignore`
* [x] Automated report generation
* [x] Git & GitHub workflow



## Week 2 — AI Automation Fundamentals

## Week 2 — AI Automation Fundamentals

- [Named Entity Recognition](Week2/Named_Entity_Recognition) — Extracts persons, dates, locations, and organizations from text as structured JSON using the Gemini API.
- [System Prompt Roles](Week2/SystemPrompt_Roles) — CLI tool with 3 configurable AI personas (Python code reviewer, Urdu/English translator, strict grammar corrector) via system prompts.
- [Token Management](Week2/Token_Management) — Notes and scripts on token counting and API cost estimation.
- [AI Text Processing Toolkit](Week2/AI_Text_Processing_Toolkit) — 5 AI-powered functions (summarize, translate, fix grammar, extract keywords, classify sentiment) using the Gemini API with structured JSON output.
- [Mini Chatbot](Week2/Mini_Chatbot) — CLI chatbot using the Gemini API with markdown-stripped output.

-------------------------------------------------------------------------
More projects will be added as the learning journey continues.
