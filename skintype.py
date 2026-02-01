from extensions import db

class SkinType(db.Model):
    __tablename__ = "skintypes"

    TypeID = db.Column(db.Integer, primary_key=True)
    TypeName = db.Column(db.String(50), nullable=False, unique=True)
    Description = db.Column(db.Text, nullable=True)

    # العلاقة بين SkinType و User
    users = db.relationship("User", backref="skin_type", lazy=True)

    def __repr__(self):
        return f"<SkinType ID={self.TypeID}, Name={self.TypeName}>"
