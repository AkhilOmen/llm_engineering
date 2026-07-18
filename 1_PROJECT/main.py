from generic_utils import fetch_website_content
from openai_utils import openai_analyze_text


if __name__ == '__main__':
    # fetch_website_content(url="https://www.cricbuzz.com/")
    website_text: str = fetch_website_content(
        url="https://www.amazon.in/Voltas-Vectra-Elite-Cooling-cools-Anti-microbial/dp/B0BBFTT3YL/"
    )
    openai_analyze_text(text=website_text)

    pass