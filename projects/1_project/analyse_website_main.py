from scrapper import fetch_website_content
from utils.openai_utils import openai_text_completion


if __name__ == '__main__':
    # fetch_website_content(url="https://www.cricbuzz.com/")
    website_text: str = fetch_website_content(
        url="https://www.amazon.in/Voltas-Vectra-Elite-Cooling-cools-Anti-microbial/dp/B0BBFTT3YL/"
    )
    openai_text_completion(text=website_text)

    pass