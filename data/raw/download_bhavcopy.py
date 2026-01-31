import requests, zipfile, io, os
from datetime import datetime

DATA_DIR = "data/raw"
os.makedirs(DATA_DIR, exist_ok=True)

today = datetime.now()
ddmmyyyy = today.strftime("%d%m%Y")
yyyy = today.strftime("%Y")
mm = today.strftime("%m")

url = f"https://www.nseindia.com/content/historical/DERIVATIVES/{yyyy}/{mm}/fo{ddmmyyyy}bhav.csv.zip"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.nseindia.com/"
}

session = requests.Session()
session.get("https://www.nseindia.com", headers=headers)

r = session.get(url, headers=headers)

if r.status_code == 200:
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        z.extractall(DATA_DIR)
    print("Downloaded FO bhavcopy:", ddmmyyyy)
else:
    print("Download failed:", r.status_code)
