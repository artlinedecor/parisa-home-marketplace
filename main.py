"""
PARISA HOME (Creating Comfort) - Rasmiy Real Ma'lumotlarga Asoslangan Backend
Brendlar: Parisa Home, Esteri, Verona Home
Telefon: +998 97 115 46 66 (Ikrom Tursunxo'jayev)
Telegram: @Tursunkhojaev_i, @ilyos_parisa
Kanal: https://t.me/parisa_home_esteri
Manzil: Tashkent, Goody, 100123, Tashkent Region (https://maps.app.goo.gl/tH5SmJKzrXd6pTM86)
"""
import os
import json
import uuid
import datetime
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="PARISA HOME ESTERI Marketplace API",
    description="Parisa, Esteri va Verona Home rasmiy mahsulotlari: Xalatlar, Sochiqlar, Mehmonxona to'plamlari, Uzum Nasiya, Click va Payme",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

DATA_DIR = "/tmp/parisa_data" if "VERCEL" in os.environ else os.path.join(BASE_DIR, "data")
try:
    os.makedirs(DATA_DIR, exist_ok=True)
except Exception:
    DATA_DIR = "/tmp"

ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")

MEMORY_ORDERS: List[Dict[str, Any]] = []
MEMORY_CHATS: List[Dict[str, Any]] = []

def load_json(filepath: str, default: Any):
    if not os.path.exists(filepath):
        return default
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def save_json(filepath: str, data: Any):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

# --- REAL KANALDAGI KATEGORIYALAR ---
CATEGORIES = [
    {"id": "all", "name": "Barcha Mahsulotlar"},
    {"id": "robes", "name": "Havana & Hotel Xalatlar"},
    {"id": "towels", "name": "Banni & Yuz Sochiqlar"},
    {"id": "hotel_collection", "name": "Mehmonxona & SPA To'plamlari"},
    {"id": "bedding", "name": "EMEN Original Choyshablar"}
]

# --- KANAL VA MSSG.ME ASOSIDAGI REAL MAHSULOTLAR ---
PRODUCTS = [
    # 1. Model-D.272 Havana Xalat (Kanal real posti)
    {
        "id": "parisa-havana-robe",
        "title": "Havana Premium Velur Xalat (Model D.272)",
        "brand": "Parisa Home",
        "category": "robes",
        "category_name": "Havana & Hotel Xalatlar",
        "price": 540000,
        "old_price": 680000,
        "badge": "Model D.272 • 600 gr/m²",
        "rating": 4.9,
        "reviews_count": 142,
        "material": "100% Paxta veluri • Qalinligi 600 gr/m²",
        "sizes": ["M", "L", "XL", "2XL"],
        "colors": ["Zumrad Yashil", "Krem Bej", "Qor Oq"],
        "uzum_installment": {
            "3_months": 198000,
            "6_months": 108000,
            "12_months": 59400
        },
        "image": "https://cdn4.telesco.pe/file/g5hxFAJ25SLWf4B-P1usBmdtUx3A7dsYEXn19hUl0q48U-qL-GNKXebwFrePaVBH_okIXFKfZ_bRfBUEajdgGHUuOdSxiBcvEAYuViTVz_WTbxt-i-LIpF4U-GSuaiES51eHo0rcUcpo5E8WfbtvLbJrk4PPsHc02_FOkZBi7wFyuco27cbKao00UKZhM-2sGDjWxEw850aUoXB7_4Z_uwvPZtHHFqRIldKDZclZXUaVzlt-h6VI4TOwVoxQvyMG2leNYqIyNEifgPGHK5KtV0XeXT_jJ9CgulernwRFM5IIDEq4_KPAQ_HkpKLGJ4a-M3wLYUR3-B49Gry7zOdb2Q.jpg",
        "description": "Telegram kanaldagi rasmiy Model-D.272 Havana xalati. Qalinligi 600 gr/m², 100% tabiiy paxtadan ishlangan. Vanna va saunadan keyin qulaylik va iliqlik bag'ishlaydi."
    },
    # 2. Model-News J 250 Sochiqlar To'plami (Kanal real posti)
    {
        "id": "parisa-news-j250",
        "title": "Model-News J 250 Sochiqlar To'plami",
        "brand": "Parisa Home / Esteri",
        "category": "towels",
        "category_name": "Banni & Yuz Sochiqlar",
        "price": 340000,
        "old_price": 420000,
        "badge": "Gramaj 500 gr/m²",
        "rating": 5.0,
        "reviews_count": 89,
        "material": "100% Toza Paxta (Gramaj: 500 gr/m²)",
        "sizes": ["Banni: 70x140 sm", "Yuz: 50x90 sm"],
        "colors": ["To'q Zumrad", "Kofeyniy", "Pushti", "Moviy"],
        "uzum_installment": {
            "3_months": 124000,
            "6_months": 68000,
            "12_months": 37400
        },
        "image": "https://cdn4.telesco.pe/file/PaFl335oAFdO9239MghwaFIjr5TVM_xm1zE1dGO5xHr1QEvoxPgx37eVvzwXqXPTfNTOUeh-N3pcSpbnJbXA3NTCIuYAK2tD6zeCWlrigCfTgKwDDPL_utvZqkKDa9cjCvxTLx_R8jJ2Y2x2gfUlWlNzIX_AIeWt3UkNro4xjSxCAO-F0qE_uHjnUPShg-k32RUt3ziwRpAuZ--cwN40fziK_-besHUCGU5I9KeRYKLCBg30-gRDSNJPyBZZxbhC9QA6pZDZYr8QhxH9XeF31LNHe9e-LWwQkzKtqGVrTL7poY8ZRYjN7hfI5q4ImRSf7DBMqcftvkHdInWAePHK8Q.jpg",
        "description": "Rasmiy kanaldagi Model-News J 250 to'plami. Gramaj 500 gr/m². Banni o'lchami 70x140 sm, yuz o'lchami 50x90 sm. Suvni bir zumda shimib oladi."
    },
    # 3. Florya Yangilik Sochiqlar (Kanal real posti)
    {
        "id": "parisa-florya-set",
        "title": "Florya Yangi Kolleksiya (Banni + Yuz)",
        "brand": "Verona Home / Parisa",
        "category": "towels",
        "category_name": "Banni & Yuz Sochiqlar",
        "price": 310000,
        "old_price": 390000,
        "badge": "Yangi Model • Cheklangan Miqdor",
        "rating": 4.8,
        "reviews_count": 65,
        "material": "100% Tabiiy Paxta • Mayin Mahra",
        "sizes": ["Banni: 70x140 sm", "Yuz: 50x90 sm"],
        "colors": ["Kulrang", "Zaytun Yashil", "Sutrang"],
        "uzum_installment": {
            "3_months": 113000,
            "6_months": 62000,
            "12_months": 34100
        },
        "image": "https://cdn4.telesco.pe/file/cC6wUOuW2b8z4WN4OHLfkkBKUdND1G4gBPL71QIfOWZ68N04bm6EGztTTiaY_zL8XhRPD03YGqOhafDnanIlrbajAvcojuAuDA8Q6jaELWq9yYPoJfcUzSno3dMvqWdCgRq71IrvK3bOy9VusdI7ahhdRFC7prQ94A0QWyCY3fKaYJo7hZjY0DrbFonh-1F5MuFeAaIv3Pp9ws7wGH4i0TA4epSB9PdwvgbQXPJokb49EAzab7cnre1u5alj5BImCmSj3HUd4hTo4fWIn_vjvsdufNSykaQH6gAGKLIAVlF_sx0aB7vimvhBysc_ck5HUtEksz8PMUxRRdwEsXtlGA.jpg",
        "description": "Yangi Florya modeli. Banni 70x140, yuz 50x90 sm. 100% paxta, yuqori chidamlilik va premium to'qilish sifati."
    },
    # 4. Hotel Textile Premium Sochiqlar (Model Hotel 450-650 gr/m²)
    {
        "id": "parisa-hotel-white",
        "title": "Hotel Textile Oq Mehmonxona Sochiqlari (450-650 gr/m²)",
        "brand": "Parisa Hotel Textile",
        "category": "hotel_collection",
        "category_name": "Mehmonxona & SPA To'plamlari",
        "price": 280000,
        "old_price": 350000,
        "badge": "Mehmonxona & SPA Tanlovi",
        "rating": 5.0,
        "reviews_count": 210,
        "material": "100% Oq Paxta (450 gr/m², 550 gr/m², 650 gr/m²)",
        "sizes": ["70x140 sm (Banni)", "50x90 sm (Yuz)", "100x150 sm (Sauna)"],
        "colors": ["Qor Oq (Klassik Mehmonxona)"],
        "uzum_installment": {
            "3_months": 102000,
            "6_months": 56000,
            "12_months": 30800
        },
        "image": "https://cdn4.telesco.pe/file/Ha-3oCLttFR9eGGhCb4605yu0w_7HDazGki_fgamZYz6SZA6UBLWFq0JTIQE7nlwUdxtgKDIr7fS1ivVvGnxSCmV8W4TM0-J4SaFUnnB6WVfsgQO1SHv2-RzxZBxkvDjeHjc-GtcZ1xIChq4BAiKf5HwzqyVsdTKkUYgggpWl5V9NhCuAnKTmuGTEnlii61_QkfKl6RhuTJkMzka_wDiU3Su0ULonzSxVpmu4QN0faHBM2FVpCNouzzT0aCNDVLsaARgd2O7crDHG4tYkDN5k5YnqXGauLubSU9yOh3_jZOwKnXHjc6ASjPTy31ezoVeymKF127gnS0lYCYSGDko4Q.jpg",
        "description": "Oq sochiq — tozalik va ishonch ramzi! Mehmonxonalar, sanatoriylar, resort va SPA lar uchun maxsus ishlab chiqarilgan. Tez-tez yuvilganda ham oqligini yo'qotmaydi."
    },
    # 5. Model D.272 Havana Sauna Sochiq (100x150 sm)
    {
        "id": "parisa-havana-sauna",
        "title": "Havana Katta Sauna Sochiq (100x150 sm)",
        "brand": "Parisa Home",
        "category": "towels",
        "category_name": "Banni & Yuz Sochiqlar",
        "price": 260000,
        "old_price": 320000,
        "badge": "600 gr/m² Zichlik",
        "rating": 4.9,
        "reviews_count": 78,
        "material": "100% Organik Egey Paxtasi • 600 gr/m²",
        "sizes": ["100x150 sm"],
        "colors": ["Zumrad Yashil", "Krem", "Kulrang"],
        "uzum_installment": {
            "3_months": 95000,
            "6_months": 52000,
            "12_months": 28600
        },
        "image": "https://cdn4.telesco.pe/file/DFkTCJV7jJFoeLe2XpefNJYx-TW-rBSt9h8vFI8VDjLRux8_smhrPtUS4NAnKq0ZaB1dfXQOlrxepIrF4POSiFH-h25NQI6AswGhw-020I0FdTvh1xK54ZMhVuaMF8-2FpzgtSRtwLt71CdzplV_3nLzu8gptHylHPglMVjrD1W6Qmtk2ZGiWZwvSKVfcfv33k78VPiVDo-BNXVPH2AiTsSS0JZQcsyBa7XR6Fh4F31X0f1tdmEPknJuIN4WjIaH2cwcK6fXO7uHCscq60uzfTMGDvd5HgQtn_EMTCE7tVe4BFXieYWOyEtiQKFumaWdsc1LXdkX4mnQgeDWQTSUoA.jpg",
        "description": "Model D.272 Havana seriyasining ulkan sauna sochiqi. 100x150 sm o'lchami butun tanani o'rash uchun yetarli."
    },
    # 6. EMEN Original Pastel Yotoq Choyshabi (Kanal real posti)
    {
        "id": "parisa-emen-bedding",
        "title": "EMEN Original 2 Kishilik Pastel Yotoq To'plami",
        "brand": "EMEN Original (Parisa Home hamkori)",
        "category": "bedding",
        "category_name": "EMEN Original Choyshablar",
        "price": 290000,
        "old_price": 360000,
        "badge": "2 Kishilik Razmer",
        "rating": 4.9,
        "reviews_count": 92,
        "material": "Yuqori sifatli tabiiy paxta matosi",
        "sizes": ["Choyshab: 250x250 sm", "Ko'rpa jild: 200x230 sm", "Yostiq jild: 48x74 sm"],
        "colors": ["Jozibali Pastel 1", "Jozibali Pastel 2"],
        "uzum_installment": {
            "3_months": 106000,
            "6_months": 58000,
            "12_months": 31900
        },
        "image": "https://cdn4.telesco.pe/file/m6n9kYJ1unpzimoyV24-YHeoKHFem1S2gVblF06hIixj5F2Hc-SKptyRhmHhqrASBIKSm4mjaSM0ydb5SmhFtY6EISgdoPQKDGreeFksMx2Y_nDoLnrromolvKlB1H9dBuaBoMitIaxqaSF9mx5XYIqWnySCcSpbNW5TIN_7y4Nt3j8YDVMBMZwQEFU-mdb85MZB34hxJq7puzsji6Xl-dG4gQ3xnNleAVsp9l368XCO5BECtr9SvS-efQj_P0AHf0H4Qoe4GOQncD85JjZoj8dYHrSkGDkNt6MeVAMaQmXSS2_8sSOwt7pWsYs8JzqLvoOauvqgXEymVDKqPG921Q.jpg",
        "description": "EMEN Original firmasi yotoq to'plami. Choyshabi 250x250 sm, Ko'rpa jild 200x230 sm, Yostiq jild 48x74 sm. Nafis va sokin uyqu kafolati."
    }
]

# --- PYDANTIC SXEMALARI ---
class OrderItem(BaseModel):
    product_id: str
    title: str
    price: float
    color: Optional[str] = "Standart"
    size: Optional[str] = "Standart"
    quantity: int = 1

class ParisaOrderCreate(BaseModel):
    customer_name: str
    phone: str
    city: str
    address: str
    payment_method: str  # uzum_nasiya, click, payme, cash_on_delivery
    installment_months: Optional[int] = 0
    items: List[OrderItem]
    note: Optional[str] = ""

class AIChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

@app.get("/api/catalog")
def get_catalog():
    return {
        "brand": {
            "name": "Parisa Home Esteri",
            "tagline": "Creating Comfort • Sifat, Nafosat, Qulaylik",
            "logo": "/static/logo.png",
            "phone": "+998 97 115 46 66",
            "manager_name": "Ikrom Tursunxo'jayev (@Tursunkhojaev_i)",
            "manager_2": "Ilyos (@ilyos_parisa)",
            "telegram_channel": "https://t.me/parisa_home_esteri",
            "hotel_channel": "https://t.me/Parisa_otel",
            "whatsapp": "+998971154666",
            "location_name": "Tashkent, Goody, 100123, Tashkent Region",
            "location_url": "https://maps.app.goo.gl/tH5SmJKzrXd6pTM86"
        },
        "categories": CATEGORIES,
        "products": PRODUCTS
    }

@app.get("/api/products/{product_id}")
def get_product(product_id: str):
    p = next((x for x in PRODUCTS if x["id"] == product_id), None)
    if not p:
        raise HTTPException(status_code=404, detail="Mahsulot topilmadi")
    return p

@app.post("/api/orders")
def create_order(req: ParisaOrderCreate):
    if not req.items:
        raise HTTPException(status_code=400, detail="Savatcha bo'sh!")

    total_amount = sum(item.price * item.quantity for item in req.items)
    order_id = f"PH-{datetime.datetime.now().strftime('%y%m%d')}-{uuid.uuid4().hex[:5].upper()}"

    monthly_payment = 0
    if req.payment_method == "uzum_nasiya" and req.installment_months:
        coeffs = {3: 0.36, 6: 0.198, 12: 0.11}
        coeff = coeffs.get(req.installment_months, 1.0 / req.installment_months)
        monthly_payment = int(total_amount * coeff)

    new_order = {
        "order_id": order_id,
        "created_at": datetime.datetime.now().isoformat(),
        "customer_name": req.customer_name,
        "phone": req.phone,
        "city": req.city,
        "address": req.address,
        "payment_method": req.payment_method,
        "installment_months": req.installment_months,
        "monthly_payment": monthly_payment,
        "total_amount": total_amount,
        "status": "pending_confirmation",
        "items": [item.model_dump() for item in req.items],
        "note": req.note
    }

    MEMORY_ORDERS.insert(0, new_order)
    orders = load_json(ORDERS_FILE, [])
    orders.append(new_order)
    save_json(ORDERS_FILE, orders)

    payment_url = ""
    if req.payment_method == "uzum_nasiya":
        payment_url = f"https://nasiya.uzum.uz/checkout?order_id={order_id}&amount={total_amount}&months={req.installment_months}"
    elif req.payment_method == "click":
        payment_url = f"https://my.click.uz/services/pay?service_id=88812&merchant_id=33211&amount={total_amount}&transaction_param={order_id}"
    elif req.payment_method == "payme":
        payment_url = f"https://checkout.paycom.uz/{order_id}?amount={int(total_amount * 100)}"

    return {
        "status": "success",
        "order": new_order,
        "payment_url": payment_url,
        "message": f"Buyurtmangiz qabul qilindi! Buyurtma ID: {order_id}"
    }

@app.get("/api/orders")
def get_orders():
    disk_orders = load_json(ORDERS_FILE, [])
    combined = MEMORY_ORDERS + [o for o in disk_orders if o["order_id"] not in [m["order_id"] for m in MEMORY_ORDERS]]
    return {"orders": combined}

def parisa_ai_stylist(user_msg: str) -> Dict[str, Any]:
    msg = user_msg.lower().strip()

    if any(w in msg for w in ["nasiya", "bo'lib", "bolib", "uzum", "kredit", "oyma"]):
        return {
            "reply": """Assalomu alaykum! 🌿 **Parisa Home Esteri** da barcha premium mahsulotlarni **Uzum Nasiya** orqali boshlang'ich to'lovsiz, 3, 6 va 12 oyga bo'lib to'lash imkoniyati mavjud!

✨ Masalan:
- **Havana D.272 Xalati (540 000 so'm):**
  • 3 oyga: oyiga **198 000 so'm**dan
  • 6 oyga: oyiga **108 000 so'm**dan
  • 12 oyga: oyiga bor-yo'g'i **59 400 so'm**dan!
- **Model-News J 250 Sochiq to'plami (340 000 so'm):**
  • 12 oyga oyiga **37 400 so'm**dan!

Pasport va karta orqali darhol tasdiqlanadi. Qaysi model bo'yicha hisoblab beray?""",
            "suggested_actions": ["Havana D.272 Xalat", "Model-News J 250 Sochiq", "Uzum Nasiya bilan buyurtma"]
        }

    if any(w in msg for w in ["xalat", "havana", "d.272", "velur"]):
        return {
            "reply": """Bizning eng mashhur xalatimiz:
👑 **Model D.272 Havana Xalati (540 000 so'm):**
- Qalinligi: **600 gr/m²** (eng yuqori zichlik!)
- 100% paxta veluri, terini mayin o'rab oladi.
- Zumrad yashil, krem bej va qor oq ranglarda mavjud.
- Razmerlar: M, L, XL, 2XL.

Uzum Nasiya bilan oyiga **59 400 so'mdan** to'lab olishingiz mumkin!""",
            "suggested_actions": ["Havana Xalatni tanlash", "Razmer bo'yicha maslahat", "Savatchaga qo'shish"]
        }

    if any(w in msg for w in ["sochiq", "j 250", "florya", "hotel", "oq"]):
        return {
            "reply": """Rasmiy do'konimizdagi eng ommabop sochiqlarimiz:
1. **Model-News J 250 To'plami (340 000 so'm):** Banni (70x140 sm) + Yuz (50x90 sm), zichligi 500 gr/m².
2. **Florya Yangi Modeli (310 000 so'm):** Banni + Yuz, cheklangan miqdorda.
3. **Hotel Textile Oq Mehmonxona Sochiqlari:** 450, 550 va 650 gr/m² zichlikda, eng bardoshli oq paxta!
4. **Havana Sauna Sochiq (260 000 so'm):** 100x150 sm, 600 gr/m².

Qaysi biri sizga kerak?""",
            "suggested_actions": ["News J 250 To'plam", "Hotel Sochiqlari", "Uzum Nasiya bilan olish"]
        }

    if any(w in msg for w in ["manzil", "lokatsiya", "qayerda", "telefon", "bog'lanish", "aloqa", "nomer"]):
        return {
            "reply": """📞 **Parisa Home Esteri Rasmiy Aloqa Ma'lumotlari:**
- Telefon: **+998 97 115 46 66** (Ikrom Tursunxo'jayev)
- Telegram: **@Tursunkhojaev_i** yoki **@ilyos_parisa**
- Rasmiy Kanalimiz: **@parisa_home_esteri** (300+ obunachi, 900+ foto)
- Mehmonxona to'plamlari: **@Parisa_otel**
- Shourum manzili: **Toshkent shahri, Goody (100123)**
- Google Maps: [Xaritada Ko'rish](https://maps.app.goo.gl/tH5SmJKzrXd6pTM86)""",
            "suggested_actions": ["Telegramga o'tish", "+998 97 115 46 66 ga qo'ng'iroq", "Shourum lokatsiyasi"]
        }

    return {
        "reply": f"""Assalomu alaykum! 🌿 **Parisa Home Esteri** rasmiy do'koniga xush kelibsiz.

Men sizning shaxsiy stilist-konsultantingizman. Bosh menejerimiz: Ikrom Tursunxo'jayev (+998 97 115 46 66).
Sizga qanday yordam bera olaman?
1. **Model D.272 Havana** xalat va sochiqlar razmerini tanlash;
2. **Uzum Nasiya** orqali 3, 6 va 12 oyga bo'lib to'lashni rasmiylashtirish;
3. Mehmonxona va SPA lar uchun ulgurji oq sochiqlar buyurtmasi.

Qaysi to'plam sizni qiziqtiryapti?""",
        "suggested_actions": ["Uzum Nasiya (Bo'lib to'lash)", "Model D.272 Havana", "Shourum Manzili va Aloqa"]
    }

@app.post("/api/ai/chat")
def ai_chat(req: AIChatRequest):
    session_id = req.session_id or str(uuid.uuid4())
    user_record = {
        "id": str(uuid.uuid4()),
        "session_id": session_id,
        "sender": "user",
        "text": req.message,
        "timestamp": datetime.datetime.now().isoformat()
    }
    MEMORY_CHATS.insert(0, user_record)

    engine_res = parisa_ai_stylist(req.message)
    bot_record = {
        "id": str(uuid.uuid4()),
        "session_id": session_id,
        "sender": "parisa_ai",
        "text": engine_res["reply"],
        "suggested_actions": engine_res.get("suggested_actions", []),
        "timestamp": datetime.datetime.now().isoformat()
    }
    MEMORY_CHATS.insert(0, bot_record)

    return {
        "session_id": session_id,
        "reply": engine_res["reply"],
        "suggested_actions": engine_res.get("suggested_actions", [])
    }

@app.get("/api/ai/chats")
def get_all_chats():
    return {"chats": MEMORY_CHATS}

@app.get("/", response_class=HTMLResponse)
def index_page():
    index_path = os.path.join(BASE_DIR, "templates", "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>PARISA HOME ESTERI Marketplace running</h1>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
