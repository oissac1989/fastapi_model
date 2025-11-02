from dataclasses import asdict

from sqlalchemy import select

from fastapi_model.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='janedoe', email='teste@gmail.com', password='strongpassword123'
        )
        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == 'janedoe'))

    assert asdict(user) == {
        'id': 1,
        'username': 'janedoe',
        'email': 'teste@gmail.com',
        'password': 'strongpassword123',
        'created_at': time,
    }
