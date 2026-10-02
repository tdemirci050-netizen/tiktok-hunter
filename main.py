# language: Python, file: main.py, target: GitHub/Render, Python 3.8+
import urllib.request
import urllib.parse
import json
import time
import random

# Proxy Listesi (Buraya kendi kullanacağın proxy IP:Port adreslerini ekleyebilirsin)
PROXIES = [
    # Örnek: "IP_ADRESI:PORT",
]

def get_random_proxy():
    if not PROXIES:
        return None
    return random.choice(PROXIES)

def check_tiktok_email(email):
    url = f"https://www.tiktok.com/api/v1/web/account/register/check/email/?email={urllib.parse.quote(email)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.tiktok.com/signup",
        "Accept": "application/json, text/plain, */*"
    }
    
    proxy = get_random_proxy()
    if proxy:
        proxy_handler = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)
        
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
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

def generate_emails():
    india_first = ["rahul", "amit", "rohit", "vikram", "sandeep", "manish", "ajay", "vijay"]
    india_last = ["patel", "sharma", "gupta", "kumar", "singh", "verma"]
    mena_first = ["mohamed", "ahmed", "ali", "ibrahim", "youssef", "omar"]
    mena_last = ["khan", "al", "bin", "ahmed", "hassan", "malik"]
    
    emails = set()
    while len(emails) < 50:
        fn = random.choice(india_first + mena_first)
        ln = random.choice(india_last + mena_last)
        token = str(random.randint(2013, 2020))
        emails.add(f"{fn}.{ln}{token}@gmail.com".lower())
    return list(emails)

if __name__ == "__main__":
    print("[*] TikTok Hunter Başlatıldı...")
    target_emails = generate_emails()
    
    for email in target_emails:
        result = check_tiktok_email(email)
        if result == "AVAILABLE":
            print(f"[+] BOŞTA HESAP BULUNDU: {email}")
        elif result == "TAKEN":
            print(f"[-] Dolu: {email}")
        elif result == "RATE_LIMIT":
            print(f"[!] 429 Engeli, bekleniyor...")
            time.sleep(20)
        else:
            print(f"[-] Engellendi/Koruma: {email}")
        time.sleep(random.uniform(2.0, 4.0))
