from extensions import db

class Routine(db.Model):
    __tablename__ = "routines"

    RoutineID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey("users.UserID"), nullable=False)
    RoutineName = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.Text, nullable=True)
    Frequency = db.Column(db.String(50), nullable=True)

    # ملاحظة: لا تضع علاقة للمستخدم هنا، فهي ستصل تلقائياً باسم user_info بفضل الملف السابق
    products = db.relationship("RoutineProduct", backref="routine_data", lazy=True)