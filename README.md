# llm_engineering
## 🚀 Projects
### 1. Web Page Analysis with BeautifulSoup + OpenAI

Extracts and analyzes web page content using LLMs.

**Pipeline:**
1. Parse HTML and extract text using **BeautifulSoup**
2. Send extracted content to **OpenAI Chat Completions API**
3. Generate summaries, sentiment analysis, and insights

**Use Case:** Scrape Amazon product reviews → analyze customer sentiment, summarize feedback, and identify 
recurring themes.

▶️ analyse_website_main.py

#### -

### 2. Company Brochure Generator

Automatically generates marketing brochures for three audiences: **prospective clients**, **investors**, 
and **recruiters**.

**Tech Highlights:**
- 🌐 **Web extraction**: BeautifulSoup for content, links, and metadata
- 🤖 **Dual model setup**:
  - `minimax-m3:cloud` (Ollama Cloud) — high accuracy
  - `deepseek-r1:1.5b` (local Ollama) — privacy + speed
- ✍️ **Prompt engineering**: one-shot prompting + budget forcing
- 📡 **Streaming responses** with formatted output

▶️  brochure_generator.py


---


## 🚀 Mini Projects
### 1. AI vs AI Debate Simulator
    
Two LLMs argue autonomously — one is **argumentative**, the other **diplomatic**. Hilarious and surprising 
results.

**Features:**
- 🤖 Dual-model setup: **Groq** (`openai/gpt-oss-20b` / `openai/gpt-oss-120b`) + **Ollama** (`minimax-m3:cloud`)
- 💬 Autonomous multi-turn conversations
- 🧠 Independent conversation memory per agent
- 🎭 Configurable personalities
- 🔄 Easy model swapping

▶️  llm_s_conversations.py