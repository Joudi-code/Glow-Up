from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    UserID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False) # طول كلمة المرور
    SkinTypeID = db.Column(db.Integer, db.ForeignKey('skintypes.TypeID'), nullable=True)
    JoinDate = db.Column(db.DateTime, default=datetime.utcnow)
    IsAdmin = db.Column(db.Boolean, default=False)

    # التعديل هنا: نستخدم backref لإضافة خاصية "user_info" في جدول الروتين تلقائياً
    routines = db.relationship("Routine", backref="user_info", lazy=True)

    def __repr__(self):
        return f"<User {self.Name}>"