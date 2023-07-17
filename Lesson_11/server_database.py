from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from common.variables import *
import datetime


# Создаем движок базы данных
database_engine = create_engine(SERVER_DATABASE, echo=False, pool_recycle=7200)

# Создаем базовый класс для декларативных моделей
Base = declarative_base()


# Класс, представляющий таблицу AllUsers
class AllUsers(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    last_login = Column(DateTime, default=datetime.datetime.now)
    active_user = relationship('ActiveUsers', back_populates='user')
    login_history = relationship('LoginHistory', back_populates='user')


# Класс, представляющий таблицу ActiveUsers
class ActiveUsers(Base):
    __tablename__ = 'Active_users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'), unique=True)
    ip_address = Column(String)
    port = Column(Integer)
    login_time = Column(DateTime, default=datetime.datetime.now)
    user = relationship('AllUsers', back_populates='active_user')


# Класс, представляющий таблицу LoginHistory
class LoginHistory(Base):
    __tablename__ = 'Login_history'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    date_time = Column(DateTime, default=datetime.datetime.now)
    ip = Column(String)
    port = Column(String)
    user = relationship('AllUsers', back_populates='login_history')


class ServerStorage:
    def __init__(self):
        # Создаем таблицы, если они не существуют
        Base.metadata.create_all(database_engine)

        # Создаем сессию
        Session = sessionmaker(bind=database_engine)
        self.session = Session()

        # Очищаем таблицу Active_users
        self.session.query(ActiveUsers).delete()
        self.session.commit()

    # Функция выполняющяяся при входе пользователя, записывает в базу факт входа
    def user_login(self, username, ip_address, port):
        print(username, ip_address, port)
        # Проверяем, существует ли пользователь с таким именем в таблице AllUsers
        user = self.session.query(AllUsers).filter_by(name=username).first()
        if user:
            # Если пользователь уже существует, обновляем время последнего входа
            user.last_login = datetime.datetime.now()
        else:
            # Если пользователь не существует, создаем нового пользователя
            user = AllUsers(name=username)
            self.session.add(user)
            self.session.commit()

        # Создаем запись о факте входа в таблице Active_users
        new_active_user = ActiveUsers(user_id=user.id, ip_address=ip_address, port=port,
                                      login_time=datetime.datetime.now())
        self.session.add(new_active_user)

        # Сохраняем вход в историю в таблице Login_history
        history = LoginHistory(user_id=user.id, date_time=datetime.datetime.now(),
                               ip=ip_address, port=port)
        self.session.add(history)

        # Сохраняем изменения
        self.session.commit()

    # Функция фиксирующая отключение пользователя
    def user_logout(self, username):
        # Получаем пользователя, который выходит
        user = self.session.query(AllUsers).filter_by(name=username).first()

        # Удаляем пользователя из таблицы Active_users
        self.session.query(ActiveUsers).filter_by(user_id=user.id).delete()

        # Применяем изменения
        self.session.commit()

    # Функция возвращает список известных пользователей со временем последнего входа.
    def users_list(self):
        query = self.session.query(AllUsers.name, AllUsers.last_login)
        return query.all()

    # Функция возвращает список активных пользователей
    def active_users_list(self):
        query = self.session.query(AllUsers.name, ActiveUsers.ip_address, ActiveUsers.port,
                                   ActiveUsers.login_time).join(ActiveUsers.user)
        return query.all()

    # Функция возвращающая историю входов по пользователю или всем пользователям
    def login_history(self, username=None):
        query = self.session.query(AllUsers.name, LoginHistory.date_time, LoginHistory.ip,
                                   LoginHistory.port).join(LoginHistory.user)
        if username:
            query = query.filter(AllUsers.name == username)
        return query.all()


# Отладка
if __name__ == '__main__':
    test_db = ServerStorage()
    # выполняем 'подключение' пользователя
    test_db.user_login('client_1', '192.168.1.4', 8888)
    test_db.user_login('client_2', '192.168.1.5', 7777)
    # выводим список кортежей - активных пользователей
    print(test_db.active_users_list())
    # выполянем 'отключение' пользователя
    test_db.user_logout('client_1')
    # выводим список активных пользователей
    print(test_db.active_users_list())
    # запрашиваем историю входов по пользователю
    test_db.login_history('client_1')
    # выводим список известных пользователей
    print(test_db.users_list())
