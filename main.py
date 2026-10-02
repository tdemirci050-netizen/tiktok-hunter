# language: Python, file: main.py, target: GitHub Actions
import urllib.request
import urllib.parse
import json
import time
import random

# Geonode'dan kopyaladığın URL'yi buraya yapıştırabilirsin
PROXY_URL = "https://proxylist.geonode.com/api/proxy-list?country=IN&protocols=http%2Chttps&filterLastChecked=60&page=1&limit=500&sort_by=responseTime&sort_type=asc"

def fetch_proxies():
    try:
        req = urllib.request.Request(PROXY_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            proxies = []
            for item in data.get("data", []):
                ip = item.get("ip")
                port = item.get("port")
                protocols = item.get("protocols", [])
                if ip and port and ("http" in protocols or "https" in protocols):
                    proxies.append(f"{ip}:{port}")
            return proxies
    except Exception:
        return []

def check_tiktok_email(email, proxies):
    url = f"https://www.tiktok.com/api/v1/web/account/register/check/email/?email={urllib.parse.quote(email)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Referer": "https://www.tiktok.com/signup",
        "Accept": "application/json, text/plain, */*"
    }
    
    proxy = random.choice(proxies) if proxies else None
    opener = urllib.request.build_opener()
    
    if proxy:
        try:
            proxy_handler = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
            opener = urllib.request.build_opener(proxy_handler)
        except Exception:
            pass
            
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with opener.open(req, timeout=10) as response:
            res_data = response.read().decode("utf-8")
            res_json = json.loads(res_data)
            is_registered = res_json.get("data", {}).get("is_registered")
            if is_registered == 0:
                return "AVAILABLE"
            elif is_registered == 1:
                return "TAKEN"
            return "UNKNOWN"
    except urllib.error.HTTPError as e:
        if e.code == 429:
            return "RATE_LIMIT"
        return f"HTTP_{e.code}"
    except Exception:
        return "BLOCKED"

def generate_target_emails():
    india_first = ["rahul", "amit", "rohit", "vikram", "sandeep", "manish", "ajay", "vijay", "sachin", "karan"]
    india_last = ["patel", "sharma", "gupta", "kumar", "singh", "verma", "yadav", "jain", "reddy"]
    
    mena_first = ["mohamed", "ahmed", "ali", "ibrahim", "youssef", "omar", "tariq", "bilal", "hamza", "zain"]
    mena_last = ["khan", "al", "bin", "ahmed", "hassan", "malik", "mansour", "nasser", "saeed"]
    
    emails = set()
    while len(emails) < 20:
        fn = random.choice(india_first + mena_first)
        ln = random.choice(india_last + mena_last)
        token = str(random.randint(1990, 2005))
        emails.add(f"{fn}.{ln}{token}@gmail.com".lower())
        
    return list(emails)

if __name__ == "__main__":
    print("[*] Proxy Listesi Alınıyor...")
    proxies = fetch_proxies()
    print(f"[*] Toplam {len(proxies)} adet proxy yüklendi.")
    
    target_emails = generate_target_emails()
    print(f"[*] Toplam {len(target_emails)} adet e-posta taranıyor...\n")
    
    for email in target_emails:
        result = check_tiktok_email(email, proxies)
        if result == "AVAILABLE":
            print(f"[+] BOŞTA HESAP BULUNDU: {email}")
        elif result == "TAKEN":
            print(f"[-] Dolu: {email}")
        elif result == "RATE_LIMIT":
            print(f"[!] 429 Hız Sınırı, bekleniyor...")
            time.sleep(10)
        else:
            print(f"[!] Durum: {email} -> {result}")
        
        time.sleep(random.uniform(2.0, 4.0))
