#!/usr/bin/env python3
"""
Instagram Avtomat Bot
- Bepul rasm olish (Pexels API)
- Post + Story joylash
- GitHub Actions bilan har kuni avtomat ishga tushadi
"""

import os
import random
import requests
from datetime import datetime
from instagrapi import Client

# ========== SOZLAMALAR (GitHub Secrets dan) ==========
INSTAGRAM_USERNAME = os.environ.get('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.environ.get('INSTAGRAM_PASSWORD')
PEXELS_API_KEY = os.environ.get('PEXELS_API_KEY')

# Mavzular: avtomobillar + motivatsiya
TOPICS = [
    'luxury car', 'sports car', 'supercar', 'exotic car',
    'car motivation', 'success motivation', 'luxury lifestyle',
    'dream car', 'entrepreneur motivation', 'millionaire mindset'
]

# Caption shablonlari (tasodifiy tanlanadi)
CAPTIONS = [
    "🏎️ Har kuni o'zingizni rivojlantiring! Sizning orzuingizdagi avtomobil sizni kutmoqda. 💪\n\n#cars #motivation #success #luxury #supercar",
    "🔥 Muvaffaqiyat yo'li oson emas, lekin har bir qadam sizni maqsadingizga yaqinlashtiradi! 🚗\n\n#motivation #cars #luxurylife #goals #dreamcar",
    "💎 Orzular katta bo'lishi kerak! Bugun qilgan harakatingiz ertangi muvaffaqiyatingiz kalitidir. 🏁\n\n#success #cars #motivation #millionaire #luxury",
    "🚀 Hech qachon to'xtamang! Sizning chegaringiz faqat sizning fikringizdir. 🏎️\n\n#nevergiveup #cars #motivation #luxury #supercar",
    "⭐ Katta maqsadlar qo'ying va ularga erishish uchun har kuni mehnat qiling! 🚗💨\n\n#goals #cars #motivation #success #luxurylifestyle"
]

SESSION_FILE = 'session.json'
CONTENT_DIR = 'content'


def download_image():
    """Pexels'dan bepul rasm yuklab olish"""
    os.makedirs(CONTENT_DIR, exist_ok=True)
    
    topic = random.choice(TOPICS)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"content_{timestamp}.jpg"
    
    try:
        headers = {"Authorization": PEXELS_API_KEY}
        params = {
            "query": topic,
            "per_page": 20,
            "orientation": "square"  # Instagram uchun optimal
        }
        
        response = requests.get(
            "https://api.pexels.com/v1/search",
            headers=headers,
            params=params,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("photos"):
                # Tasodifiy rasm tanlash
                photo = random.choice(data["photos"])
                img_url = photo["src"]["large"]
                
                # Rasmni yuklab olish
                img_response = requests.get(img_url, timeout=30)
                if img_response.status_code == 200:
                    filepath = os.path.join(CONTENT_DIR, filename)
                    with open(filepath, 'wb') as f:
                        f.write(img_response.content)
                    print(f"✅ Rasm yuklandi: {filename} (Mavzu: {topic})")
                    return filepath
                    
    except Exception as e:
        print(f"❌ Rasm yuklash xato: {e}")
    
    return None


def login_instagram():
    """Instagram'ga login, session saqlash"""
    cl = Client()
    
    try:
        # Avvalgi session'ni yuklash
        if os.path.exists(SESSION_FILE):
            cl.load_settings(SESSION_FILE)
            cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
            print("✅ Session'dan login qilindi")
        else:
            # Yangi login
            cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
            cl.dump_settings(SESSION_FILE)
            print("✅ Yangi login, session saqlandi")
        return cl
        
    except Exception as e:
        print(f"❌ Login xato: {e}")
        # Yangi urinish
        try:
            cl = Client()
            cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
            cl.dump_settings(SESSION_FILE)
            return cl
        except Exception as e2:
            print(f"❌ Ikkinchi urinish xato: {e2}")
            return None


def post_content(cl, image_path):
    """Post va story joylash"""
    caption = random.choice(CAPTIONS)
    
    try:
        # POST joylash
        print("📤 Post joylanmoqda...")
        cl.photo_upload(image_path, caption)
        print(f"✅ Post joylandi: {datetime.now().strftime('%H:%M:%S')}")
        
        # STORY joylash (shu rasm bilan)
        print("📤 Story joylanmoqda...")
        cl.photo_upload_to_story(image_path)
        print(f"✅ Story joylandi: {datetime.now().strftime('%H:%M:%S')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Joylash xato: {e}")
        return False


def main():
    """Asosiy funksiya"""
    print(f"\n{'='*60}")
    print(f"🤖 Instagram Avtomat Bot ishga tushdi!")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # 1. Rasm yuklash
    image_path = download_image()
    if not image_path:
        print("❌ Rasm olinmadi! Bot to'xtatildi.")
        return
    
    # 2. Instagram'ga login
    cl = login_instagram()
    if not cl:
        print("❌ Instagram'ga ulanib bo'lmadi!")
        return
    
    # 3. Post va story joylash
    success = post_content(cl, image_path)
    
    if success:
        print(f"\n{'='*60}")
        print(f"✅ Barcha operatsiyalar muvaffaqiyatli tugadi!")
        print(f"{'='*60}\n")
    else:
        print(f"\n{'='*60}")
        print(f"⚠️ Ba'zi operatsiyalar bajarilmadi")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
