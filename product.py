from extensions import db

class Product(db.Model):
    __tablename__ = "products"

    ProductID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    Category = db.Column(db.String(100), nullable=False)
    Price = db.Column(db.Float, nullable=False)
    Description = db.Column(db.Text, nullable=True)
    Image = db.Column(db.String(255), nullable=True)
    
    # السطر المفقود الذي سبب المشكلة:
    Ingredients = db.Column(db.Text, nullable=True) 

    AdminID = db.Column(db.Integer, db.ForeignKey("admins.AdminID"), nullable=True)

    def __repr__(self):
        return f"<Product {self.Name}>"