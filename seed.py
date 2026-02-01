from app import app
from extensions import db
from models.skintype import SkinType
from models.product import Product
from models.admin import Admin
from werkzeug.security import generate_password_hash

def seed_data():
    with app.app_context():
        print("⏳ جاري تصفير قاعدة البيانات وإضافة كافة المنتجات الـ 20 بالترتيب...")
        db.session.query(Product).delete()
        db.session.query(SkinType).delete()
        db.session.commit()

        # إضافة أنواع البشرة
        for name in ['Oily', 'Dry', 'Combination', 'Sensitive']:
            db.session.add(SkinType(TypeName=name, Description=f"Routine for {name} skin"))

        # القائمة الكاملة المرتبة (الترتيب هنا يحدد الـ ID)
        products = [
            {   # ID: 1
                "Name": "Anua Heartleaf Quercetinol Pore Deep Cleansing Foam",
                "Category": "غسول للبشرة الدهنية والمختلطة",
                 "Price": 20.0,
                "Image": "/static/images/Anua heartleaf quercetinol pore deep cleansing foam.jpg",
                "Ingredients": "مستخلص الهارت ليف، حمض الساليسيليك (BHA).",
                "Desc": "غسول رغوي عميق ينظف المسام بفعالية."
            },
            {   # ID: 2
                "Name": "Anua Heartleaf 77% Soothing Toner",
                "Category": "تونر مهدئ للبشرة",
                 "Price": 18.0,
                "Image": "/static/images/Anua - Heartleaf 77 - Verzachtende toner, 250ml-Geen kleur.jpg",
                "Ingredients": "77% مستخلص الهارت ليف، بانثينول، بيتين.",
                "Desc": "التونر الأكثر مبيعاً لتهدئة البشرة وموازنة حموضتها."
            },
            {   # ID: 3
                "Name": "Anua Heartleaf Pore Control Cleansing Oil",
                "Category": "زيت منظف للمسام",
                 "Price": 22.0,
                "Image": "/static/images/ANUA Heartleaf Pore Control Cleansing Oil _ K-Beauty Gentle Makeup Remover.jpg",
                "Ingredients": "زيوت نباتية، مستخلص الهارت ليف، تركيبة غير سادة للمسام.",
                "Desc": "يزيل المكياج والرؤوس السوداء والشوائب الزيتية."
            },
            {   # ID: 4
                "Name": "Anua Heartleaf 70 Daily Lotion",
                "Category": "مرطب للبشرة الدهنية والمختلطة", 
                "Price": 26.0,
                "Image": "/static/images/مرطب بشرة دهنية ومختلطة.jpg",
                "Ingredients": "هارت ليف، حمض الهيالورونيك الثلاثي.",
                "Desc": "لوشن خفيف جداً يمنح ترطيباً عميقاً دون ثقل."
            },
            {   # ID: 5
                "Name": "Skin1004 Madagascar Centella Air-Fit Suncream Light",
                "Category": "واقي شمسي للبشرة الدهنية", 
                "Price": 16.20,
                "Image": "/static/images/واقي شمسي بشرة دهنية.jpg",
                "Ingredients": "مستخلص السنتيلا، نياسيناميد، أكسيد الزنك.",
                "Desc": "واقي شمس فيزيائي مهدئ وخفيف جداً."
            },
            {   # ID: 6
                "Name": "Anua Azelaic Acid 10 Hyaluron Redness Soothing Serum",
                "Category": "سيروم لعلاج حب الشباب", 
                "Price": 24.0,
                "Image": "/static/images/Anua Azelaic Acid 15+ Intense Calming Serum (Ingredients Explained).jpg",
                "Ingredients": "حمض الأزيليك، نياسيناميد، هارت ليف.",
                "Desc": "يعالج الاحمرار وآثار الحبوب والحبوب النشطة."
            },
            {   # ID: 7
                "Name": "Dr. Althea's 345 Relief Cream",
                "Category": "كريم مهدئ لعلاج الآثار", 
                "Price": 18.90,
                "Image": "/static/images/Dr_Althea 345 Relief Cream 50ml _ Shopee Brasil.jpg",
                "Ingredients": "سنتيلا، نياسيناميد، بانثينول، سيراميد.",
                "Desc": "كريم فعال جداً لترميم حاجز البشرة المتضرر."
            },
            {   # ID: 8
                "Name": "Anua Niacinamide 10% + TXA 4% Serum",
                "Category": "سيروم لعلاج التصبغات", 
                "Price": 24.0,
                "Image": "/static/images/سيروم انوا للتصبغات.jpg",
                "Ingredients": "نياسيناميد 10%، حمض الترانيكساميك (TXA) 4%.",
                "Desc": "سيروم قوي جداً لتفتيح البقع الداكنة وتوحيد اللون."
            },
            {   # ID: 9
                "Name": "SKIN1004 Madagascar Centella Ampoule Foam",
                "Category": "غسول للبشرة الجافة والحساسة", 
                "Price": 12.60,
                "Image": "/static/images/غسول بشرة حساسة (2).jpg",
                "Ingredients": "مستخلص السنتيلا، منظفات مستخلصة من جوز الهند.",
                "Desc": "غسول لطيف لا يجرد البشرة من زيوتها الطبيعية."
            },
            {   # ID: 10
                "Name": "Anua Heartleaf Silky Moisture Sunscreen SPF 50+",
                "Category": "واقي شمسي للبشرة الجافة", 
                "Price": 18.0,
                "Image": "/static/images/واقي شمسي للبشرة الجافة.jpg",
                "Ingredients": "هارت ليف، مرطبات حريرية، فلاتر كيميائية آمنة.",
                "Desc": "يوفر حماية عالية مع ملمس كريمي مرطب."
            },
            {   # ID: 11
                "Name": "Anua Heartleaf 70% Intense Calming Cream",
                "Category": "مرطب للبشرة الجافة", 
                "Price": 26.0,
                "Image": "/static/images/مرطب بشرة جافة.jpg",
                "Ingredients": "70% هارت ليف، سيراميد، بانثينول.",
                "Desc": "كريم غني ومركز لترطيب البشرة الجافة جداً."
            },
            {   # ID: 12
                "Name": "SKIN1004 Madagascar Centella Ampoule",
                "Category": "سيروم للبشرة الجافة والحساسة", 
                "Price": 19.0,
                "Image": "/static/images/سيروم بشرة حساسة.jpg",
                "Ingredients": "100% مستخلص سنتيلا آسياتيكا نقي.",
                "Desc": "يهدئ البشرة فوراً ويرطبها بعمق."
            },
            {   # ID: 13
                "Name": "Madagascar Centella Hyalu-Cica Water-Fit Sun Serum",
                "Category": "واقي شمسي للبشرة المختلطة", 
                "Price": 23.0,
                "Image": "/static/images/واقي شمسي بشرة مختلطة.jpg",
                "Ingredients": "هيالورونيك، سنتيلا، ماء أوراق البتولا.",
                "Desc": "أفضل واقي شمس بقوام مائي خفيف جداً."
            },
            {   # ID: 14
                "Name": "Madagascar Centella Hyalu-Cica Blue Serum",
                "Category": "سيروم للبشرة المختلطة", 
                "Price": 19.80,
                "Image": "/static/images/سيروم بشرة مختلطة.jpg",
                "Ingredients": "مركب هيالو-سيكا، 5 أنواع من حمض الهيالورونيك.",
                "Desc": "سيروم مائي يمنح توهجاً وترطيباً فورياً."
            },
            {   # ID: 15
                "Name": "SKIN1004 Madagascar Centella Soothing Cream",
                "Category": "مرطب للبشرة الحساسة", 
                "Price": 14.40,
                "Image": "/static/images/مرطب بشرة حساسة.jpg",
                "Ingredients": "سنتيلا، سيراميد (EOP, NS, NP).",
                "Desc": "كريم جل مهدئ يبرد البشرة ويصلح حاجزها."
            }
        ]

        for p in products:
            db.session.add(Product(
                Name=p['Name'], Category=p['Category'], Price=p['Price'],
                Image=p['Image'], Ingredients=p['Ingredients'], Description=p['Desc']
            ))

        if not Admin.query.filter_by(Email="admin@glowup.com").first():
            db.session.add(Admin(Name="Admin", Email="admin@glowup.com", Password=generate_password_hash("admin123")))

        db.session.commit()
        print(" قاعدة البيانات جاهزة الآن بالكامل (20 منتج) مع المكونات والترتيب!")

if __name__ == "__main__": seed_data()