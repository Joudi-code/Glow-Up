from extensions import db

class RoutineProduct(db.Model):
    __tablename__ = "routine_products"

    ID = db.Column(db.Integer, primary_key=True)
    RoutineID = db.Column(db.Integer, db.ForeignKey("routines.RoutineID"), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey("products.ProductID"), nullable=False)

    # إضافة هذه السطور لضمان الربط السليم
    product = db.relationship("Product", backref="product_routines")