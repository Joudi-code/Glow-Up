from app import app
from extensions import db


from models.user import User
from models.admin import Admin
from models.product import Product
from models.skintype import SkinType
from models.routine import Routine
from models.routine_product import RoutineProduct

if __name__ == "__main__":
    with app.app_context():
        print(" جاري إنشاء جداول قاعدة البيانات...")
        db.create_all()
        print(" تم إنشاء جميع الجداول بنجاح!")