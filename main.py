# language: Python, file: main.py, target: GitHub Actions
import urllib.request
import urllib.parse
import json
import time
import random

# Eğer elinde ücretsiz proxy'ler varsa buraya "IP:Port" şeklinde ekleyebilirsin.
# Boş bırakırsan doğrudan kendi sunucu IP'si ile dener (ancak test için iyidir).
PROXIES = [
    # "IP_ADRESI:PORT",
]

def get_random_proxy():
    if not PROXIES:
        return None
    return random.choice(PROXIES)

def check_tiktok_email(email):
    url = f"https://www.tiktok.com/api/v1/web/account/register/check/email/?email={urllib.parse.quote(email)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
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
                return "AVAILABLE" # BOŞTA (Hesap açılabilir)
            elif is_registered == 1:
                return "TAKEN"     # DOLU (Zaten hesap var)
            return "UNKNOWN"
    except urllib.error.HTTPError as e:
        if e.code == 429:
            return "RATE_LIMIT"
        return f"HTTP_{e.code}"
    except Exception:
        return "BLOCKED"

def generate_target_emails():
    # Hint ve MENA (Arap) bölgesi popüler isim soyisim kalıpları
    india_first = ["rahul", "amit", "rohit", "vikram", "sandeep", "manish", "ajay", "vijay", "sachin", "karan"]
    india_last = ["patel", "sharma", "gupta", "kumar", "singh", "verma", "yadav", "jain", "reddy"]
    
    mena_first = ["mohamed", "ahmed", "ali", "ibrahim", "youssef", "omar", "tariq", "bilal", "hamza", "zain"]
    mena_last = ["khan", "al", "bin", "ahmed", "hassan", "malik", "mansour", "nasser", "saeed"]
    
    emails = set()
    # Her çalıştırmada rastgele 30 farklı kombinasyon üretir
    while len(emails) < 30:
        fn = random.choice(india_first + mena_first)
        ln = random.choice(india_last + mena_last)
        token = str(random.randint(1990, 2005))
        emails.add(f"{fn}.{ln}{token}@gmail.com".lower())
        
    return list(emails)

if __name__ == "__main__":
    print("[*] TikTok Hunter (Hint & MENA) Taraması Başlatıldı...")
    target_emails = generate_target_emails()
    print(f[*] Toplam {len(target_emails)} adet e-posta hedefi oluşturuldu ve taranıyor...\n")
    
    for email in target_emails:
        result = check_tiktok_email(email)
        if result == "AVAILABLE":
            print(f"[+] BOŞTA HESAP BULUNDU: {email}")
        elif result == "TAKEN":
            print(f"[-] Dolu: {email}")
        elif result == "RATE_LIMIT":
            print(f"[!] 429 Hız Sınırı (Rate Limit) yendi, bekleniyor...")
            time.sleep(15)
        else:
            print(f"[!] Koruma / Engel: {email} (Durum: {result})")
        
        # Bot gibi görünmemek için istekler arası rastgele bekleme süresi
        time.sleep(random.uniform(3.0, 6.0))
