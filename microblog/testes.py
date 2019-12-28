from app.models import User


def test_user():
    u = User(username='franc', email='franc@example.com')
    print(u)


if __name__ == "__main__":
    test_user()
