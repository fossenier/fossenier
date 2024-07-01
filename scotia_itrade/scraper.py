from google import search
import requests

query = 'site:scotiabank.com "fund facts" filetype:pdf'
pdf_links = []

for url in search(query, num=20, stop=20, pause=2):
    if url.endswith(".pdf"):
        pdf_links.append(url)

for pdf_link in pdf_links:
    print(pdf_link)
