from extensions import db


class Ingredient(db.Model):
    __tablename__ = "ingredients"

    IngredientID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Benefit = db.Column(db.Text, nullable=True)

    ProductID = db.Column(db.Integer, db.ForeignKey("products.ProductID"), nullable=False)

    product = db.relationship("Product", backref=db.backref("ingredients", lazy=True))

    def __repr__(self):
        return f"<Ingredient {self.Name}>"
