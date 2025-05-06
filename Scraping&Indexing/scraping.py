import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin, urlparse
import base64
import networkx as nx
import pandas as pd

def sanitize_filename(url):
    """Sanitizes a URL to create a valid and somewhat readable filename using Base64 encoding."""
    encoded_url = base64.b64encode(url.encode('utf-8')).decode('utf-8')
    safe_filename = encoded_url.replace('/', '_').replace('+', '-')
    return safe_filename

def scrape_and_save(url, output_dir="scraped_pages"):
    """Scrapes the content of a URL and saves it to a file with the URL as the first line."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        text_content = soup.get_text(separator='\n', strip=True)

        filename = sanitize_filename(url) + ".txt"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(url + "\n")
            f.write(text_content)

        return True
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return False
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return False

def find_links(url):
    """Finds all the links on a given webpage."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = [urljoin(url, a.get('href')) for a in soup.find_all('a', href=True)]
        return list(set(links))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url} for links: {e}")
        return []
    except Exception as e:
        print(f"Error processing {url} for links: {e}")
        return []

def calculate_pagerank(link_graph):
    """
    Calculates PageRank for a given link graph.
    Returns a dictionary of URLs and their PageRank scores.
    """
    G = nx.DiGraph()
    
    # Add nodes and edges to the graph
    for url, links in link_graph.items():
        G.add_node(url)
        for link in links:
            if link in link_graph:  # Only add links to pages we've crawled
                G.add_edge(url, link)
    
    # Calculate PageRank
    pr = nx.pagerank(G, alpha=0.85)  # alpha is the damping factor
    
    return pr

if __name__ == "__main__":
    start_url = "https://developer.mozilla.org/en-US/"
    output_directory = "scraped_pages"
    os.makedirs(output_directory, exist_ok=True)

    visited_links = set()
    queue = [start_url]
    links_processed = 0
    max_links = 10  # Limiting for demonstration
    
    # Store link relationships for PageRank
    link_graph = {}

    print(f"Starting scraping from: {start_url}")

    while queue and links_processed < max_links:
        current_url = queue.pop(0)

        if current_url in visited_links:
            continue

        print(f"Processing: {current_url} ({links_processed + 1}/{max_links})")
        if scrape_and_save(current_url, output_directory):
            links_processed += 1

        new_links = find_links(current_url)

        # Only store links that are in queue or visited (i.e., actually crawled or will be)
        link_graph[current_url] = [link for link in new_links if link in visited_links or link in queue]

        for link in new_links:
            if link.startswith("http") and link not in visited_links and link not in queue:
                queue.append(link)

        visited_links.add(current_url)

    print(f"\nScraping finished. Processed {links_processed} links.")
    print(f"Saved content to the '{output_directory}' directory.")

    # Calculate and display PageRank
    print("\nCalculating PageRank...")
    pagerank_scores = calculate_pagerank(link_graph)
    
    # Sort by PageRank score (descending)
    sorted_pagerank = sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)
    
    print("\nPageRank Results:")
    print("Rank\tScore\tURL")
    for rank, (url, score) in enumerate(sorted_pagerank, 1):
        print(f"{rank}\t{score:.6f}\t{url}")
    
    # Save PageRank results to CSV (append mode)
    df = pd.DataFrame(sorted_pagerank, columns=['URL', 'PageRank'])
    df.to_csv('pagerank_results.csv', mode='a', header=not os.path.exists('pagerank_results.csv'), index=False)
    print("\nSaved PageRank results to 'pagerank_results.csv'")
