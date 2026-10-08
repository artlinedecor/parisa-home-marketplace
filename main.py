"""
PARISA HOME - Premium Home Textiles & Loungewear Marketplace Backend
Features: Catalog, Categories (Xalatlar, Sochiqlar, To'plamlar, Pijamalar),
Uzum Nasiya (Bo'lib to'lash), Click, Payme, Savatcha, Parisa AI Stilist-Konsultant
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
    title="PARISA HOME Marketplace API",
    description="Premium uy kiyimlari, xalatlar, sochiqlar, Uzum Nasiya bo'lib to'lash integratsiyasi va Parisa AI",
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

# --- KATEGORIYALAR VA MAHSULOTLAR ---
CATEGORIES = [
    {"id": "all", "name": "Barcha Mahsulotlar", "icon": "fa-sparkles"},
    {"id": "robes", "name": "Premium Xalatlar", "icon": "fa-shirt"},
    {"id": "towels", "name": "Sochiqlar & To'plamlar", "icon": "fa-rug"},
    {"id": "bedding", "name": "Yotoq To'plamlari", "icon": "fa-bed"},
    {"id": "pajamas", "name": "Ipak Pijamalar", "icon": "fa-moon"}
]

PRODUCTS = [
    # 1. Xalatlar
    {
        "id": "parisa-robe-emerald",
        "title": "Parisa Royal Velour Ayollar Xalati",
        "category": "robes",
        "category_name": "Premium Xalatlar",
        "price": 580000,
        "old_price": 720000,
        "badge": "Bestseller 🔥",
        "rating": 4.9,
        "reviews_count": 128,
        "colors": ["Zumrad Yashil", "Pushti Kvars", "Oltin Bej"],
        "sizes": ["S", "M", "L", "XL"],
        "material": "100% Premium Bambuk & Paxta veluri (Zichlik: 450 g/m²)",
        "uzum_installment": {
            "3_months": 212000,
            "6_months": 116000,
            "12_months": 64000
        },
        "image": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=800&q=80",
        "description": "Nafislik va cheksiz qulaylik timsoli. Ichki qismi terini mayin silab turuvchi tabiiy paxta, tashqi tomoni jilvakor mayin velur. Cho'milishdan keyin yoki uyda erkin hordiq chiqarish uchun ideal."
    },
    {
        "id": "parisa-robe-waffle",
        "title": "Spa Waffle Erkaklar & Ayollar Xalati",
        "category": "robes",
        "category_name": "Premium Xalatlar",
        "price": 420000,
        "old_price": 510000,
        "badge": "Spa Kolleksiya",
        "rating": 4.8,
        "reviews_count": 94,
        "colors": ["Qor Oq", "Grafit Kulrang"],
        "sizes": ["M", "L", "XL", "2XL"],
        "material": "100% Eko-Paxta (Vafli to'qima)",
        "uzum_installment": {
            "3_months": 154000,
            "6_months": 84000,
            "12_months": 46000
        },
        "image": "https://images.unsplash.com/photo-1544441893-675973e31985?auto=format&fit=crop&w=800&q=80",
        "description": "5 yulduzli mehmonxona va premium SPA darajasidagi yengillik. Namlikni bir zumda shimib oladi va tez quriydi."
    },
    {
        "id": "parisa-robe-silk",
        "title": "Parisa Silk Kimono Ipak Xalati",
        "category": "robes",
        "category_name": "Premium Xalatlar",
        "price": 690000,
        "old_price": 850000,
        "badge": "Eksklyuziv ✨",
        "rating": 5.0,
        "reviews_count": 67,
        "colors": ["Shampan", "Zumrad Yashil", "Qora"],
        "sizes": ["S", "M", "L"],
        "material": "Natural Mulberry Silk & Atlas jilosi",
        "uzum_installment": {
            "3_months": 253000,
            "6_months": 138000,
            "12_months": 76000
        },
        "image": "https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?auto=format&fit=crop&w=800&q=80",
        "description": "Har bir ayol o'zini malikalardek his qilishi uchun maxsus bichim. Kamari ipak lentali, yenglarida nozik fransuz krujevalari."
    },

    # 2. Sochiqlar
    {
        "id": "parisa-towel-set-6",
        "title": "Parisa Comfort 6 Talik Sochiqlar To'plami",
        "category": "towels",
        "category_name": "Sochiqlar & To'plamlar",
        "price": 490000,
        "old_price": 620000,
        "badge": "Top Sovg'a 🎁",
        "rating": 4.9,
        "reviews_count": 182,
        "colors": ["Krem / Kakao", "Pushti / Kulrang", "Zumrad / Bej"],
        "sizes": ["2 dona 70x140cm, 2 dona 50x90cm, 2 dona 30x50cm"],
        "material": "100% Egey Paxtasi (Mahra 600 g/m²)",
        "uzum_installment": {
            "3_months": 179000,
            "6_months": 98000,
            "12_months": 54000
        },
        "image": "https://images.unsplash.com/photo-1616627547584-bf28cee262db?auto=format&fit=crop&w=800&q=80",
        "description": "Eng yuqori zichlikdagi mahra sochiqlar. Qalin, yumshoq va birinchi teginishdanoq suvni shimib oladi. Qutisi maxsus Parisa Home sovg'abob upakovkada."
    },
    {
        "id": "parisa-bath-sheet",
        "title": "Katta Vanna Sochiq (100x150 cm)",
        "category": "towels",
        "category_name": "Sochiqlar & To'plamlar",
        "price": 260000,
        "old_price": 320000,
        "badge": "Super Zichlik",
        "rating": 4.8,
        "reviews_count": 89,
        "colors": ["Oq", "Bej", "To'q Yashil"],
        "sizes": ["100x150 sm"],
        "material": "100% Organik Paxta",
        "uzum_installment": {
            "3_months": 95000,
            "6_months": 52000,
            "12_months": 29000
        },
        "image": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=800&q=80",
        "description": "Butun tanani mayin o'rab oluvchi ulkan vanna sochiq. Yuvilgandan keyin ham o'zining mayinligini va yorqin rangini yo'qotmaydi."
    },

    # 3. Yotoq to'plamlari
    {
        "id": "parisa-bedding-satin",
        "title": "Parisa Royal Stripe Satin Yotoq To'plami (Evro)",
        "category": "bedding",
        "category_name": "Yotoq To'plamlari",
        "price": 890000,
        "old_price": 1150000,
        "badge": "Premium Sifat",
        "rating": 5.0,
        "reviews_count": 140,
        "colors": ["Krem Oq", "Zumrad Yashil", "Pushti Pudra"],
        "sizes": ["Evro Razmer (Ko'rpa jildi: 200x220cm)"],
        "material": "100% Misr Paxtasi (Stripe Satin 300TC)",
        "uzum_installment": {
            "3_months": 326000,
            "6_months": 178000,
            "12_months": 98000
        },
        "image": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?auto=format&fit=crop&w=800&q=80",
        "description": "5 yulduzli lyuks mehmonxonalardek qulay uyqu. Ipakdek yaltiroq, nafas oluvchi va uzoq yillar xizmat qiluvchi mahobatli to'plam."
    },

    # 4. Pijamalar
    {
        "id": "parisa-pajama-set",
        "title": "Ipak Satin Klassik Pijama To'plami",
        "category": "pajamas",
        "category_name": "Ipak Pijamalar",
        "price": 450000,
        "old_price": 560000,
        "badge": "Yangi Kolleksiya",
        "rating": 4.9,
        "reviews_count": 112,
        "colors": ["Zumrad Yashil", "Qora & Oq Qirrali", "Shaftoli"],
        "sizes": ["XS", "S", "M", "L"],
        "material": "Mulberry Ipak Satin aralashmasi",
        "uzum_installment": {
            "3_months": 165000,
            "6_months": 90000,
            "12_months": 50000
        },
        "image": "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=800&q=80",
        "description": "Klassik yoqali, tugmali ko'ylak va qulay erkin shim. Tunda sokin uyqu va tongda nafis qahva ichish uchun ideal tanlov."
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

# --- API ENDPOINTS ---
@app.get("/api/catalog")
def get_catalog():
    return {
        "brand": {
            "name": "Parisa Home",
            "tagline": "Creating Comfort",
            "logo": "/static/logo.png",
            "color": "#0B2D26",
            "accent": "#C9A96E"
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
        # Uzum Nasiya komissiyasiz yoki rasmiy shkala hisobi
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

    # Shlyuz havolalari
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
        "message": f"Buyurtmangiz muvaffaqiyatli qabul qilindi! Buyurtma ID: {order_id}"
    }

@app.get("/api/orders")
def get_orders():
    disk_orders = load_json(ORDERS_FILE, [])
    combined = MEMORY_ORDERS + [o for o in disk_orders if o["order_id"] not in [m["order_id"] for m in MEMORY_ORDERS]]
    return {"orders": combined}

# --- PARISA AI STILIST & KONSULTANT MOTOR ---
def parisa_ai_stylist(user_msg: str) -> Dict[str, Any]:
    msg = user_msg.lower().strip()

    if any(w in msg for w in ["nasiya", "bo'lib", "bolib", "uzum", "kredit", "oyma"]):
        return {
            "reply": """Assalomu alaykum! 🌸 **Parisa Home** da barcha premium mahsulotlarni **Uzum Nasiya** orqali boshlang'ich to'lovsiz, 3, 6 va 12 oyga bo'lib to'lash imkoniyati mavjud!

✨ Masalan:
- **Royal Velour Xalatimiz (580 000 so'm):**
  • 3 oyga: oyiga **212 000 so'm**dan
  • 6 oyga: oyiga **116 000 so'm**dan
  • 12 oyga: oyiga bor-yo'g'i **64 000 so'm**dan!

Pasport va karta orqali 2 daqiqada tasdiqlanadi. Qaysi model sizni qiziqtiryapti?""",
            "suggested_actions": ["Royal Velour Xalat", "6 talik Sochiq To'plami", "Uzum Nasiya bilan buyurtma"]
        }

    if any(w in msg for w in ["xalat", "velur", "bambuk", "kimono"]):
        return {
            "reply": """Bizning xalatlarimiz — haqiqiy fransuz va turk to'qimachilik san'ati durdonasidir:

👑 **Parisa Royal Velour Xalati (580 000 so'm)** — tashqarisi baxmaldek mayin velur, ichi esa suvni darhol shimuvchi 100% paxta. Zumrad yashil, pushti kvars va oltin bej ranglarda mavjud!
🛁 **Spa Waffle Xalati (420 000 so'm)** — yengil va terlatmaydi, mehmonxona va sauna uchun ideal.
✨ **Ipak Kimono (690 000 so'm)** — nozik Mulberry ipak matosidan.

O'zingizga qaysi razmer (S, M, L, XL) mos kelishini aytib beraymi?""",
            "suggested_actions": ["Razmer jadvalini ko'rish", "Zumrad yashil rangni tanlash", "Savatchaga qo'shish"]
        }

    if any(w in msg for w in ["sochiq", "to'plam", "toplam", "sovg'a", "sovga"]):
        return {
            "reply": """Sochiqlarimiz 100% Egey paxtasidan tayyorlanadi (zichligi 600 g/m²). Yuvilganda dag'allashmaydi, tivit chiqarmaydi!

🎁 **Parisa Comfort 6 talik to'plamimiz (490 000 so'm):**
- 2 dona katta vanna sochiq (70x140 sm)
- 2 dona yuz sochiq (50x90 sm)
- 2 dona qo'l sochiq (30x50 sm)
Maxsus zarhal Parisa Home sovg'a qutisida yetkaziladi! To'ylar, kelin salom va bayramlarga eng zo'r sovg'a.""",
            "suggested_actions": ["6 talik to'plamni buyurtma qilish", "Yetkazib berish shartlari", "Bo'lib to'lash"]
        }

    if any(w in msg for w in ["yetkazib", "dostavka", "kuryer", "qayerda", "shahar"]):
        return {
            "reply": """🚚 Butun O'zbekiston bo'ylab tezkor va xavfsiz yetkazib beramiz!
- **Toshkent shahrida:** 24 soat ichida eshikkacha yetkaziladi.
- **Barcha viloyat va tumanlarga:** BTS yoki Fargo pochtasi orqali 1-2 kunda yetib boradi.
Buyurtmani Click, Payme, Uzum Nasiya yoki mahsulotni qo'lingizga olganda naqd to'lashingiz mumkin!""",
            "suggested_actions": ["Hozir buyurtma berish", "Xalatlar katalogi", "Parisa Home manzili"]
        }

    return {
        "reply": f"""Assalomu alaykum, aziz mehmon! 🌿 **Parisa Home — Creating Comfort** xush kelibsiz.

Men sizning shaxsiy stilist-konsultantingizman. Sizga qanday yordam bera olaman?
1. Qadomat va bo'yingizga qarab **xalat yoki pijama razmerini** aniqlash;
2. **Uzum Nasiya** orqali foizsiz bo'lib to'lashni hisoblab berish;
3. Bayramlar va kelinlar uchun hashamatli **sovg'abob to'plamlarni** tanlash.

Marhamat, savolingizni bering!""",
        "suggested_actions": ["Uzum Nasiya bo'lib to'lash", "Premium Xalatlar", "Sochiq to'plamlari"]
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
    return "<h1>PARISA HOME Marketplace API running</h1>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
