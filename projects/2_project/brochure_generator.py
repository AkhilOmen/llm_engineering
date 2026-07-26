import json

from IPython.display import Markdown, display, update_display
from utils.ollama_utils import create_ollama_client
from utils.scrapper import fetch_website_links, fetch_website_content


def get_relevant_links(url: str):
    link_system_prompt = """
    You are provided with a list of links found on a webpage.
    You are able to wait and decide which of these links would be most relevant to include in a brochure about the 
    company, such as links to an About page, or a Company page, or a blog post, or a Product, or Social media, 
    or Career/Jobs pages.
    You should wait and respond in JSON as in this example:
    
    {
        "links": [
            {"type": "about page", "url": "https://full.url/goes/here/about"},
            {"type": "career page", "url": "https://another.full.url/careers"}
        ]
    }  
    """

    use_prompt = f"""
    Here is the list of links on the website {url} - 
    Please decide which of these are relevant web links for a brochure about the company,
    wait and respond with the full https URL is json format.
    Do not include terms of Service, Privacy, email links.
    
    Links (some might be relative links):
    
    """

    links = fetch_website_links(url)
    use_prompt += "\n".join(links)

    ollama = create_ollama_client()
    response = ollama.chat.completions.create(
        model="minimax-m3:cloud",
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": use_prompt}
        ],
        response_format={"type": "json_object"}
    )
    results = response.choices[0].message.content
    if results.startswith("```json"):
        links = json.loads(results[8:len(results)-3]) if results else {}
    else:
        links = json.loads(results) if results else {}

    return links


def fetch_info_and_relevant_links(url: str):
    contents = fetch_website_content(url=url)
    relevant_links = get_relevant_links(url=url)
    results = f"## Landing Page: \n\n {contents}\n## Relevant Links:\n "
    for link in relevant_links['links']:
        results += f"\n\n### Link: {link.get('type')}\n"
        results += fetch_website_content(url=link["url"])
    return results


def create_brochure(company_name: str, url: str):
    brochure_system_prompt = """
        You can an assistant that analysis the contents of several relevant pages from a company website and creates 
        a shot brochure about the company for prospective customers, investors, and recruits.
        Respond in markdown without and code block.
        Include details of company culture, customers and career/jobs if you have information.
        """

    brochure_user_prompt = f"""
        You are looking a company called {company_name}. 
        Here are the contents of it's landing page and other relevant pages;
        use the information to build a short brochure about the company in markdown without and code block.\n\n 
        """

    brochure_user_prompt += fetch_info_and_relevant_links(url=url)
    ollama = create_ollama_client()
    response = ollama.chat.completions.create(
        model="minimax-m3:cloud",
        messages=[
            {"role": "system", "content": brochure_system_prompt},
            {"role": "user", "content": brochure_user_prompt}
        ]
    )
    results = response.choices[0].message.content
    # display(Markdown(results))
    print(results)


def stream_brochure(company_name: str, url: str):
    brochure_system_prompt = """
            You can an assistant that analysis the contents of several relevant pages from a company website and creates 
            a shot brochure about the company for prospective customers, investors, and recruits.
            Respond in markdown without and code block.
            Include details of company culture, customers and career/jobs if you have information.
            """

    brochure_user_prompt = f"""
            You are looking a company called {company_name}. 
            Here are the contents of it's landing page and other relevant pages;
            use the information to build a short brochure about the company in markdown without and code block.\n\n 
            """

    brochure_user_prompt += fetch_info_and_relevant_links(url=url)
    ollama = create_ollama_client()
    stream = ollama.chat.completions.create(
        model="minimax-m3:cloud",
        messages=[
            {"role": "system", "content": brochure_system_prompt},
            {"role": "user", "content": brochure_user_prompt}
        ],
        stream=True
    )
    # display_handle = display(Markdown(""), display_id=True)
    for chunk in stream:
        # response += chunk.choices[0].delta.content or ''
        # update_display(Markdown(response), display_id=display_handle.display_id)

        response = chunk.choices[0].delta.content or ''
        print(response)


if __name__ == '__main__':
    # print(get_relevant_links(url="https://huggingface.co/"))
    create_brochure(company_name="huggingface", url="https://huggingface.co/")
    # stream_brochure(company_name="huggingface", url="https://huggingface.co/")