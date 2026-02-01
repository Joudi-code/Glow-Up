from flask import Flask, request, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_cors import CORS
from config.config import Config
from extensions import db, migrate, jwt

# App Setup
app = Flask(__name__)
CORS(app) 
app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)

# Import Models
from models.user import User
from models.admin import Admin
from models.product import Product
from models.skintype import SkinType

# Admin Creation Helper
def create_admin_if_not_exists():
    if not Admin.query.filter_by(Email="admin@glowup.com").first():
        db.session.add(Admin(
            Name="Admin",
            Email="admin@glowup.com",
            Password=generate_password_hash("admin123")
        ))
        db.session.commit()
        print("✅ Admin account ready.")

def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({"message": "Admins only!"}), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

# HTML Routes
@app.route('/')
def index(): return render_template('index.html')
@app.route('/login')
def login(): return render_template('login.html')
@app.route('/signup')
def signup(): return render_template('signup.html')
@app.route('/products')
def products(): return render_template('products.html')
@app.route('/product-details')
def product_details(): return render_template('product-details.html')
@app.route('/skintest')
def skintest(): return render_template('skintest.html')
@app.route('/routine')
def routine(): return render_template('routine.html')
@app.route('/admin')
def admin_dashboard(): return render_template('admin.html')

# --- APIs ---

@app.route('/api/signup', methods=['POST'])
def api_signup():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    
    if User.query.filter_by(Email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    st_id = None
    if data.get('skin_type'):
        st = SkinType.query.filter(SkinType.TypeName.ilike(data.get('skin_type'))).first()
        if st: st_id = st.TypeID

    new_user = User(
        Name=data.get('name'),
        Email=email,
        Password=generate_password_hash(data.get('password').strip()),
        SkinTypeID=st_id
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()

    # 1. فحص المستخدمين
    user = User.query.filter_by(Email=email).first()
    if user and check_password_hash(user.Password, password):
        token = create_access_token(identity=str(user.UserID), additional_claims={"role": "user"})
        
        # --- جلب اسم نوع البشرة ---
        skin_type_name = ""
        if user.SkinTypeID:
            st = SkinType.query.get(user.SkinTypeID)
            if st: skin_type_name = st.TypeName.lower() # تحويله لأحرف صغيرة
        # -------------------------------------------

        return jsonify({
            "status": "success",
            "access_token": token,
            "role": "user",
            "username": user.Name,
            "skin_type": skin_type_name # نرسل النوع للمتصفح
        }), 200

    # 2. فحص الأدمن
    admin = Admin.query.filter_by(Email=email).first()
    if admin and check_password_hash(admin.Password, password):
        token = create_access_token(identity=str(admin.AdminID), additional_claims={"role": "admin"})
        return jsonify({
            "status": "success",
            "access_token": token,
            "role": "admin",
            "username": admin.Name,
            "skin_type": "" # الأدمن ليس لديه بشرة
        }), 200

    return jsonify({"status": "fail", "message": "البريد أو كلمة المرور خطأ"}), 401


@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        "id": p.ProductID, "name": p.Name, "category": p.Category,
        "price": p.Price, "image": p.Image, "description": p.Description
    } for p in products]), 200

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    p = Product.query.get(product_id)
    if not p: return jsonify({"message": "Product not found"}), 404
    return jsonify({
        "id": p.ProductID, "name": p.Name, "category": p.Category,
        "price": p.Price, "image": p.Image, "description": p.Description,
        "ingredients": p.Ingredients
    }), 200

@app.route('/api/skin-test', methods=['POST'])
@jwt_required()
def skin_test():
    data = request.get_json()
    user = User.query.get(int(get_jwt_identity()))
    if not user: return jsonify({"message": "User not found"}), 404

    st = SkinType.query.filter(SkinType.TypeName.ilike(data.get("skin_type"))).first()
    if st:
        user.SkinTypeID = st.TypeID
        db.session.commit()
        return jsonify({"message": "Skin type updated", "skin_type": st.TypeName}), 200
    return jsonify({"message": "Unknown type"}), 400

# Admin Actions
@app.route('/api/admin/users', methods=['GET'])
@admin_required
def get_all_users():
    users = User.query.all()
    result = []
    for u in users:
        if u.Email == "admin@glowup.com": continue
        skin = "Unknown"
        if u.SkinTypeID:
            st = SkinType.query.get(u.SkinTypeID)
            if st: skin = st.TypeName
        result.append({
            "name": u.Name, "email": u.Email, "skin_type": skin,
            "join_date": u.JoinDate.strftime('%Y-%m-%d') if u.JoinDate else "N/A"
        })
    return jsonify(result), 200

@app.route('/api/admin/users/<string:email>', methods=['DELETE'])
@admin_required
def delete_user(email):
    user = User.query.filter_by(Email=email).first()
    if not user: return jsonify({"message": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_product(product_id):
    p = Product.query.get(product_id)
    if not p: return jsonify({"message": "Product not found"}), 404
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 200

@app.route('/api/admin/products', methods=['POST'])
@admin_required
def add_product():
    data = request.get_json()
    new_p = Product(
        Name=data['name'], Category=data['category'], Price=data['price'],
        Description=data['description'], Image=data['image'], AdminID=int(get_jwt_identity())
    )
    db.session.add(new_p)
    db.session.commit()
    return jsonify({"message": "Product added"}), 201

@app.route('/api/admin/products/<int:product_id>', methods=['PUT'])
@admin_required
def update_product(product_id):
    data = request.get_json()
    p = Product.query.get(product_id)
    if not p: return jsonify({"message": "Product not found"}), 404
    
    p.Name = data.get('name', p.Name)
    p.Category = data.get('category', p.Category)
    p.Price = data.get('price', p.Price)
    p.Description = data.get('description', p.Description)
    db.session.commit()
    return jsonify({"message": "Product updated"}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_admin_if_not_exists()
    app.run(debug=True)
