import requests, zipfile, io, os
from datetime import datetime, timedelta

DATA_DIR = "data/raw"
os.makedirs(DATA_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.nseindia.com/"
}

def make_url(d: datetime) -> str:
    ddmmyyyy = d.strftime("%d%m%Y")
    yyyy = d.strftime("%Y")
    mm = d.strftime("%m")
    return f"https://www.nseindia.com/content/historical/DERIVATIVES/{yyyy}/{mm}/fo{ddmmyyyy}bhav.csv.zip"

def try_download_for_date(session: requests.Session, d: datetime) -> bool:
    url = make_url(d)
    r = session.get(url, headers=headers, timeout=60)
    if r.status_code != 200:
        print(f"No file for {d.date()} (status {r.status_code})")
        return False

    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        z.extractall(DATA_DIR)

    print(f"Downloaded FO bhavcopy for {d.date()}")
    return True

def main():
    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers, timeout=60)  # warm-up

    # Try today, then go back up to 7 days to find last available bhavcopy (weekend/holiday safe)
    start = datetime.now()
    for i in range(0, 8):
        d = start - timedelta(days=i)
        if try_download_for_date(session, d):
            return

    # If we reach here, nothing worked -> FAIL the workflow
    raise SystemExit("Failed to download bhavcopy for the last 7 days (possible NSE block or long holiday).")

if __name__ == "__main__":
    main()
