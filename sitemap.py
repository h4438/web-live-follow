from usp.tree import sitemap_tree_for_homepage
from unidecode import unidecode
import requests
import sys
import pandas as pd
from typing import List

class SiteLinks:

    def __init__(self, name: str):
        self.sitemap = None
        self.robots = None
        self.pages = None
        self.name = name

    def set_pages(self, pages: List[str]):
        self.pages = pages
        return

    def set_robots(self, url: str):
        self.robots = url
        return

    def set_sitemap(self, url: str):
        self.sitemap = url
        return

def explore_sitemap(url: str, name: str) -> SiteLinks:
    # This function explores the sitemap of a website
    # Input: main url
    # Output: a SiteLinks objection,
    tree = sitemap_tree_for_homepage(url)
    pages = set()
    subs = tree.sub_sitemaps
    for page in tree.all_pages():
        pages.add(page)
    site = SiteLinks(name)
    try:
        site.set_sitemap(subs[1].url)
    except:
        site.set_sitemap("")
        print("-> Can't find sitemap")
    try:
        site.set_robots(subs[0].url)
    except:
        site.set_robots("")
        print("-> Can't find robots")
    site.set_pages(list(pages))
    return site

def check_website_sitemap(csv_file: str) -> List[SiteLinks]:
    # This function checks sitemap of a csv file of websites
    # Input: csv file path
    # Output:
    sites = []
    df = pd.read_csv(csv_file)
    for idx, row in df.iterrows():
        sitelink = explore_sitemap(row['link'], row['name'])
        sites.append(sitelink)
    return sites

def compare_sitemaps(site_old: List[str], site_new: List[str]) -> List[str]:
    setA = set(site_old)
    setB = set(site_new)
    differs = setA.symmetric_difference(setB)
    return list(differs)

def run_sitemap_stalking_process(csv_file: str, csv_name: str, save_folder:str):
    # This function runs the whole process of checking sitemap and saving them
    sites = check_website_sitemap(csv_file)
    df = pd.read_csv(csv_file)
    sitemaps = []
    robots = []
    total = []
    parse_sitemap_page = lambda e: {\
            "url": e.url,\
            "priority": e.priority,\
            "news_story": e.news_story,\
            "last_modified": e.last_modified,\
            "change_frequency": e.change_frequency}

    for idx in range(df.shape[0]):
        row = df.iloc[idx]
        sitemaps.append(sites[idx].sitemap)
        robots.append(sites[idx].robots)
        total.append(len(sites[idx].pages))
        # save links
        html_links = [parse_sitemap_page(page) for page in sites[idx].pages]
        html_df = pd.DataFrame(html_links)
        html_df.to_json(f"{save_folder}/{row['name']}_links.jsonl",\
                lines=True, orient='records')
    df['sitemap_url'] = sitemaps
    df["robots_url"] = robots
    df["total_pages"] = total
    file_name = unidecode(csv_name).replace(" ","_")
    df.to_json(f"{save_folder}/{file_name}.jsonl", lines=True, orient='records')
    return

if __name__ == "__main__":
    print("Hello")
    run_sitemap_stalking_process('./data/src/collection.csv', 'collection', './data/site')
