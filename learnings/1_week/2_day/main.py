import requests

from utils.gemini_utils import gemini_text_completion
from utils.ollama_utils import ollama_text_completion


if __name__ == '__main__':
    # print(gemini_text_completion(message="Tell me a fun fact"))
    # print(requests.get("http://localhost:11434").content)
    print(ollama_text_completion(
        message="100gm chicken contains what Nutrients and MicroNutrients can you list down with their quantity"
    ))
    pass