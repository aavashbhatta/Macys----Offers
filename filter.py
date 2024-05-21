from requests_html import HTMLSession
from bs4 import BeautifulSoup

url = "https://www.macys.com"

session = HTMLSession()
response = session.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    sale_occurrences = set()   # Store unique occurrences

    # Keywords to search for
    keywords = ["off"]

    # Look for occurrences of keywords in <a> tags
    for link in soup.find_all("a"):
        for keyword in keywords:
            if keyword in link.text.lower():
                sale_occurrences.add(link.text.strip())

    # Look for "off" in <div> tags with specific classes
    for div in soup.find_all("div", class_=["sale", "discount"]):
        if "off" in div.text.lower():
            sale_occurrences.add(div.text.strip())

    # Occurrences
    if sale_occurrences:
        html_content = "<html><head><title>Occurrences</title></head><body>"
        html_content += "<h1>Offers for Macys</h1>"
        html_content += "<ul>"
        for occurrence in sale_occurrences:
            html_content += f"<li>{occurrence}</li>"
        html_content += "</ul>"
        html_content += "</body></html>"

        with open("sale_occurrences.html", "w") as file:
            file.write(html_content)

        print("HTML file 'sale_occurrences.html' has been created successfully.")
    else:
        print("No occurrences of the word 'sale' found on the page.")
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
