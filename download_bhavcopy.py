import requests
import zipfile
import io
import os
from datetime import datetime, timedelta

DATA_DIR = "data/raw"
os.makedirs(DATA_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.nseindia.com/"
}

def make_url(d):
    ddmmyyyy = d.strftime("%d%m%Y")
    yyyy = d.strftime("%Y")
    mm = d.strftime("%m")
    return f"https://www.nseindia.com/content/historical/DERIVATIVES/{yyyy}/{mm}/fo{ddmmyyyy}bhav.csv.zip"

def try_download(session, d):
    url = make_url(d)
    print(f"Trying: {url}")

    r = session.get(url, headers=HEADERS, timeout=60)

    if r.status_code != 200:
        print(f"No bhavcopy for {d.date()} (status {r.status_code})")
        return False

    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        z.extractall(DATA_DIR)

    print(f"Downloaded bhavcopy for {d.date()}")
    return True

def main():
    session = requests.Session()

    # Warm-up request (important for NSE)
    session.get("https://www.nseindia.com", headers=HEADERS, timeout=60)

    # Try today, then go back up to 7 days (weekend / holiday safe)
    today = datetime.now()
    for i in range(0, 8):
        d = today - timedelta(days=i)
        if try_download(session, d):
            return

    # If nothing worked, FAIL the workflow
    raise SystemExit("❌ No NSE FO bhavcopy found in last 7 days")

if __name__ == "__main__":
    main()
