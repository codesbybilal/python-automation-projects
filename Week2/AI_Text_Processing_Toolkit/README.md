# AI Text Processing Toolkit

A command-line toolkit with 5 AI-powered text processing functions, built using the Gemini API (`gemini-3.5-flash-lite`).

## Features

| # | Function | Description |
|---|----------|-------------|
| 1 | Text Summarizer | Summarizes text within a specified word limit |
| 2 | Translator | Translates text into any specified language |
| 3 | Grammar Fixer | Corrects grammar, spelling, and punctuation |
| 4 | Keyword Extractor | Extracts top N relevant keywords from text |
| 5 | Sentiment Classifier | Classifies sentiment (positive/negative/neutral) with a confidence score |

## Setup

1. Install dependencies:
```bash
   pip install -r requirements.txt
```
2. Create a `.env` file in this folder with your Gemini API key:
GEMINI_API_KEY=your_key_here
3. Run:
```bash
   python main.py
```

## Usage Examples

**Text Summarization**
Enter your choice (1-6): 1
Enter the text to summarize: Pakistan has a mountain range called Karakoram range which contains the second highest mountain in the world, known as K2.
Enter the number of max words in output: 10
AI: Pakistan's Karakoram range has K2, second highest in the world.

---------------------------------------------------------------

**Translation**
Enter your choice (1-6): 2
Enter the text you want to translate: Hey, how are you doing?
Enter the language to translate into: Spanish
AI: Hola, ¿cómo estás?

---------------------------------------------------------------

**Fix Grammar**
Enter your choice (1-6): 3
Enter the text to fix the grammar: How is you doin?
AI: How are you doing?

---------------------------------------------------------------

**Keyword Extraction**
Enter your choice (1-6): 4
Enter the text to extract the keywords from: Shanghai is one of the developed cities in North China
Enter the total number of top extracted keywords: 3
AI: ['Shanghai', 'developed cities', 'North China']
-------------------------------------------------------------


**Sentiment Classification**

Enter your choice (1-6): 5
Enter the text to classify its sentiment: The weather is pleasant today
AI: {'sentiment': 'positive', 'confidence': 0.99}

--------------------------------------------------------------


## Technical Notes

- Keyword extraction and sentiment classification use Gemini's structured JSON output (`response_schema`) for reliable, parseable results.
- Each of the 5 functions is independently callable and self-contained — each builds its own system prompt internally rather than relying on shared state.
- Built as part of Week 2 of an AI Automation learning roadmap, following [Week 1](../../Week1) (Python fundamentals + API basics).