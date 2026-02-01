from app import app
from models.user import User

if __name__ == "__main__":
    with app.app_context():
        users = User.query.all()
        print(f"------ عدد المستخدمين في قاعدة البيانات: {len(users)} ------")
        for u in users:
            print(f"الاسم: {u.Name} | الايميل: {u.Email} | هل هو أدمن؟: {u.IsAdmin}")
        print("------------------------------------------------")