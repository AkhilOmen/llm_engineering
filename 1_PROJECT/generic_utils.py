import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/117.0.0.0 Safari/537.36"
}

def fetch_website_content(url: str) -> str:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string if soup.title else "No Title Found"
    """
        What exactly the line from 17-18 is doing? 
        It's finding all the elements for eg: <script>console.log("Hello")</script> and removing them.  
        It also can be written as soup.body.find_all(["script", "style", "img", "input"])
    """
    for irrelevant in soup.body(["script", "style", "img", "input"]):
        irrelevant.decompose()

    text = soup.body.get_text(separator="\n", strip=True)

    # print("TITLE   " + title)
    # print("\n\n\n")
    # print("TEXT   " + text)

    return "TITLE: " + title + "\n\n\n" + text
