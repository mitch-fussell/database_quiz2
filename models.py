import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from sqlmodel import SQLModel, Field, create_engine

# Constants for scraping
BASE_URL = "https://all.rugby"
SQUAD_URL = f"{BASE_URL}/club/south-africa/squad"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; CopilotBot/1.0)"
}

engine = create_engine("sqlite:///springboks.db")

class PlayerLinksScraper:
    @staticmethod
    def get_player_links():
        resp = requests.get(SQUAD_URL, headers=HEADERS)
        soup = BeautifulSoup(resp.text, "html.parser")
        links = []
        for a in soup.select("a[href^='/player/']"):
            href = a.get("href")
            if href and href.startswith("/player/"):
                links.append(BASE_URL + href)
        return list(set(links))

class StatsTableParser:
    @staticmethod
    def parse_stats_table(soup, player_name):
        stats = []
        saison_div = soup.find("div", id="saison_2025")
        if not saison_div:
            return stats
        table = saison_div.find("table", class_="rtable JSaison")
        if not table:
            return stats
        rows = table.find("tbody").find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 15:
                continue
            team = cols[2].text.strip()
            place = cols[4].text.strip()
            result = cols[5].text.strip()
            date = cols[6].text.strip()
            number = cols[7].text.strip()
            tries = cols[8].text.strip()
            drops = cols[9].text.strip()
            penalties = cols[10].text.strip()
            conversions = cols[11].text.strip()
            points = cols[12].text.strip()
            pen_cards = cols[13].text.strip()
            minutes = cols[14].text.strip().replace("'", "")
            stats.append({
                "Player": player_name,
                "Team": team,
                "Place": place,
                "Result": result,
                "Date": date,
                "Number": number,
                "Tries": tries,
                "Drops": drops,
                "Penalties": penalties,
                "Conversions": conversions,
                "Points": points,
                "Pen_Cards": pen_cards,
                "Minutes": minutes
            })
        return stats

class PlayerNameParser:
    @staticmethod
    def get_player_name(soup):
        h1 = soup.find("h1", class_="inbl")
        if h1:
            text = h1.get_text(separator=" ", strip=True)
            text = re.sub(r"\s*\d+\s*years,.*$", "", text)
            text = re.sub(r"\s+", " ", text).strip()
            return text
        return ""

class RugbyStatsSaver:
    @staticmethod
    def scrape_and_save_stats(output_csv="stats.csv"):
        all_stats = []
        links = PlayerLinksScraper.get_player_links()
        for link in links:
            resp = requests.get(link, headers=HEADERS)
            soup = BeautifulSoup(resp.text, "html.parser")
            player_name = PlayerNameParser.get_player_name(soup)
            name_parts = player_name.split()
            if len(name_parts) > 1:
                first_name = ' '.join(name_parts[:-1])
                last_name = name_parts[-1]
            else:
                first_name = player_name
                last_name = ''
            stats = StatsTableParser.parse_stats_table(soup, player_name)
            for s in stats:
                s['FirstName'] = first_name
                s['LastName'] = last_name
            all_stats.extend(stats)
            time.sleep(1)
        df = pd.DataFrame(all_stats)
        if not df.empty:
            cols = ['FirstName', 'LastName'] + [c for c in df.columns if c not in ['FirstName', 'LastName']]
            df = df[cols]
        df.to_csv(output_csv, index=False)

class Bio(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    FirstName: str
    LastName: str
    Position: str
    Age: int
    Birthdate: str
    Height_m: float
    Weight_kg: float
    Height_ft_in: str
    Weight_st_lb: str
    Weight_lb: float

class Stats(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    FirstName: str
    LastName: str
    Player: str
    Team: str
    Place: str
    Result: str
    Date: str
    Number: str
    Tries: str
    Drops: str
    Penalties: str
    Conversions: str
    Points: str
    Pen_Cards: str
    Minutes: str
