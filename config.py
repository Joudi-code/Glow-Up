class Config:
    # غيرنا الاسم إلى glowup.db لنميزه عن الملفات القديمة
    SQLALCHEMY_DATABASE_URI = "sqlite:///glowup.db" 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "secret-key"
    JWT_SECRET_KEY = "jwt-secret-key"