# llm_engineering


**Project 1: Web Page Analysis with BeautifulSoup and OpenAI**

    Step 1: Parse the website's HTML and extract the relevant textual content using BeautifulSoup.
    Step 2: Pass the extracted content to the OpenAI Chat Completions API for intelligent analysis, 
            summarization, and insights generation.

    Use cases:
    1. Extract reviews from an e-commerce product page (e.g., Amazon) and use the OpenAI 
       Chat Completions API to analyze customer sentiment, summarize feedback, and identify 
       common themes.


**Project 2: Company sales Boucher Generator**
    
    Objective - 
    Create a product that can generate marketing broucher about a company;
    1. For prospective clients
    2. For investors
    3. For recruiters

    Tech Used -
    1. Open Source model
        ) "minimax-m3:cloud" hosted on Ollama Cloud – Primary model with excellent accuracy.
        ) "deepseek-r1:1.5b" hosted locally using Ollama – lower accuracy compared to "minimax-m3".
    2. Web Content Extraction
        ) BeautifulSoup for extracting website content, links, and relevant company information.
    3. Prompt Engineering
        ) Used budget forcing
        ) Implemented one-shot prompting
    4. Streaming Responses
        ) Streamed LLM responses in real time with formatted output
