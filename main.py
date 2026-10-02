# language: Python, file: main.py, target: GitHub Actions
import urllib.request
import urllib.parse
import json
import time
import random

def check_tiktok_email_mobile(email):
    # TikTok mobil uygulamasının kayıt/kontrol API uç noktası
    url = f"https://api16-normal-useast5.tiktokv.com/passport/email/check_email_registered/?email={urllib.parse.quote(email)}"
    
    # Gerçek bir iPhone / TikTok mobil uygulamasından atılıyormuş gibi simüle edilen başlıklar
    headers = {
        "User-Agent": "com.zhiliaoapp.musically/28.3.4 (iPhone; iOS 16.6; Scale/3.00)",
        "sdk-version": "2",
        "app-type": "normal",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "accept-encoding": "gzip, deflate"
    }
    
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = response.read().decode("utf-8")
            res_json = json.loads(res_data)
            
            # Mobil API yanıt yapısı kontrolü
            data = res_json.get("data", {})
            is_registered = data.get("is_registered")
            
            if is_registered == 0:
                return "AVAILABLE" # BOŞTA (Kayıtlı değil)
            elif is_registered == 1:
                return "TAKEN"     # DOLU (Kayıtlı)
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
    while len(emails) < 25:
        fn = random.choice(india_first + mena_first)
        ln = random.choice(india_last + mena_last)
        token = str(random.randint(1990, 2005))
        emails.add(f"{fn}.{ln}{token}@gmail.com".lower())
        
    return list(emails)

if __name__ == "__main__":
    print("[*] TikTok Mobil API Tarayıcısı Başlatıldı...")
    target_emails = generate_target_emails()
    print(f"[*] Toplam {len(target_emails)} adet e-posta taranıyor...\n")
    
    for email in target_emails:
        result = check_tiktok_email_mobile(email)
        if result == "AVAILABLE":
            print(f"[+] BOŞTA HESAP BULUNDU: {email}")
        elif result == "TAKEN":
            print(f"[-] Dolu (Kayıtlı): {email}")
        elif result == "RATE_LIMIT":
            print(f"[!] 429 Hız Sınırı, bekleniyor...")
            time.sleep(10)
        else:
            print(f"[!] Durum: {email} -> {result}")
        
        # Mobil API istekleri arasında ban yememek için kısa bekleme
        time.sleep(random.uniform(1.5, 3.0))
