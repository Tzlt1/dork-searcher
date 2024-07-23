import requests
from urllib.parse import quote
from bs4 import BeautifulSoup

def get_sql_dorks(keywords_file, dorks_file, max_pages=10):
    """
    Get SQL dorks from Google search results.

    Args:
        keywords_file (str): File containing keywords to search for.
        dorks_file (str): File to write dorks to.
        max_pages (int): Maximum number of search result pages to scrape. Default is 10.

    Returns:
        None
    """
    with open(keywords_file, 'r') as f:
        keywords = [line.strip() for line in f.readlines()]

    dorks = set()  # Use a set to avoid duplicates
    for keyword in keywords:
        query = f"site:.gov inurl:(php?id= OR php?cat=) intitle:{quote(keyword)} intext:{quote(keyword)} | inurl:(asp?id= OR asp?cat=) intitle:{quote(keyword)} intext:{quote(keyword)} | inurl:(jsp?id= OR jsp?cat=) intitle:{quote(keyword)} intext:{quote(keyword)}"
        for page in range(max_pages):
            url = f"https://www.google.com/search?q={quote(query)}&start={page * 10}"
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for result in soup.find_all('div', class_='rc'):
                    anchors = result.find_all('a')
                    if anchors:
                        link = anchors[0]['href']
                        if link.startswith('http'):  # Filter out non-HTTP links
                            dorks.add(link)
            else:
                break  # Stop scraping if we get a non-200 status code

    with open(dorks_file, 'w') as f:
        for dork in dorks:
            f.write(dork + "\n")

get_sql_dorks("keywords.txt", "sql_dorks.txt", max_pages=20)
