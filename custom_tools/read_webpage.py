import requests
from bs4 import BeautifulSoup
import re

def read_webpage(url: str) -> str:
    response = requests.get(url)
    webpage_text = BeautifulSoup(response.text).get_text()
    # Remove multiple empty lines
    webpage_text = re.sub(r'\n\s*\n', '\n\n', webpage_text)
    return webpage_text