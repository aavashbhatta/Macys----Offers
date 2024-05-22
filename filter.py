import requests
from bs4 import BeautifulSoup
import json

payload = { 'api_key': 'fc49a37ba26ff7139932713ecc1b9d03', 'url': 'https://www.macys.com' }

r = requests.get('https://api.scraperapi.com/', params=payload)

response = r

#url = "https://www.macys.com"
#headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36" }
#response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    sale_occurrences = set()   # store unique occurrences

    # keywords
    keywords = ["off"]
    restricted_words = ["coffee", "office"]

    # function to check if text contains any restricted words
    def contains_restricted_word(text, restricted_words):
        return any(word in text for word in restricted_words)

    # look for occurrences of keywords in <a> tags
    for link in soup.find_all("a"):
        text = link.text.lower().strip()
        if any(keyword in text for keyword in keywords) and not contains_restricted_word(text, restricted_words):
            sale_occurrences.add(link.text.strip())

    # look for "off" in <div> tags with specific classes
    for div in soup.find_all("div", class_=["sale", "discount"]):
        text = div.text.lower().strip()
        if "off" in text and not contains_restricted_word(text, restricted_words):
            sale_occurrences.add(div.text.strip())

  
    json_data = [{"title": occurrence} for occurrence in sale_occurrences]

    
    with open("sale_occurrences.json", "w") as file:
        json.dump(json_data, file, indent=4)

    print("JSON file 'sale_occurrences.json' has been created successfully.")
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
