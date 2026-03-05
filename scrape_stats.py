
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

BASE_URL = "https://all.rugby"
SQUAD_URL = f"{BASE_URL}/club/south-africa/squad"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; CopilotBot/1.0)"
}

def get_player_links():
    resp = requests.get(SQUAD_URL, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")
    links = []
    for a in soup.select("a[href^='/player/']"):
        href = a.get("href")
        if href and href.startswith("/player/"):
            links.append(BASE_URL + href)
    return list(set(links))

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
        # Tournament = cols[1].text.strip()  # Skipped
        team = cols[2].text.strip()
        # Opponent = cols[3].text.strip()  # Skipped
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

def get_player_name(soup):
    h1 = soup.find("h1", class_="inbl")
    if h1:
        # Remove any <img> and trailing text (age, position)
        text = h1.get_text(separator=" ", strip=True)
        # Remove age/position (e.g., "26 years, Prop")
        text = re.sub(r"\s*\d+\s*years,.*$", "", text)
        # Remove any double spaces
        text = re.sub(r"\s+", " ", text).strip()
        return text
    return ""

def main():
    all_stats = []
    links = get_player_links()
    for link in links:
        resp = requests.get(link, headers=HEADERS)
        soup = BeautifulSoup(resp.text, "html.parser")
        player_name = get_player_name(soup)
        # Split full name into first and last name
        name_parts = player_name.split()
        if len(name_parts) > 1:
            first_name = ' '.join(name_parts[:-1])
            last_name = name_parts[-1]
        else:
            first_name = player_name
            last_name = ''
        stats = parse_stats_table(soup, player_name)
        # Add first and last name columns
        for s in stats:
            s['FirstName'] = first_name
            s['LastName'] = last_name
        all_stats.extend(stats)
        time.sleep(1)  # Be polite to the server
    df = pd.DataFrame(all_stats)
    # Place FirstName and LastName as first columns
    if not df.empty:
        cols = ['FirstName', 'LastName'] + [c for c in df.columns if c not in ['FirstName', 'LastName']]
        df = df[cols]
    df.to_csv("stats.csv", index=False)

if __name__ == "__main__":
    main()
