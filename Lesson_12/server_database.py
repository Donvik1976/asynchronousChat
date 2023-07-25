from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from common.variables import *
import datetime


# Создаем движок базы данных
database_engine = create_engine('sqlite:///server_base.db3', echo=False, pool_recycle=7200,
                                connect_args={'check_same_thread': False})

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


# Класс, представляющий таблицу контактов пользователей
class UsersContacts(Base):
    __tablename__ = 'Contacts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    contact_id = Column(Integer, ForeignKey('Users.id'))
    user = relationship('AllUsers', back_populates='contacts', foreign_keys=[user_id])
    contact = relationship('AllUsers', back_populates='contacts', foreign_keys=[contact_id])


# Класс, представляющий таблицу истории действий
class UsersHistory(Base):
    __tablename__ = 'History'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    sent = Column(Integer)
    accepted = Column(Integer)
    user = relationship('AllUsers', back_populates='history')


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

        # Создаем запись в таблице контактов
        contact = UsersContacts(user_id=user.id, contact_id=user.id)
        self.session.add(contact)

        # Создаем запись в таблице истории действий
        user_history = UsersHistory(user_id=user.id, sent=0, accepted=0)
        self.session.add(user_history)

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

    # Функция фиксирует передачу сообщения и делает соответствующие отметки в БД
    def process_message(self, sender, recipient):
        sender_obj = self.session.query(AllUsers).filter_by(name=sender).first()
        recipient_obj = self.session.query(AllUsers).filter_by(name=recipient).first()

        if not sender_obj or not recipient_obj:
            return

        sender_history = self.session.query(UsersHistory).filter_by(user_id=sender_obj.id).first()
        recipient_history = self.session.query(UsersHistory).filter_by(user_id=recipient_obj.id).first()

        sender_history.sent += 1
        recipient_history.accepted += 1

        self.session.commit()

    # Функция добавляет контакт для пользователя.
    def add_contact(self, user, contact):
        user_obj = self.session.query(AllUsers).filter_by(name=user).first()
        contact_obj = self.session.query(AllUsers).filter_by(name=contact).first()
        if not contact_obj or self.session.query(UsersContacts).\
                filter_by(user_id=user_obj.id, contact_id=contact_obj.id).count():
            return

        new_contact = UsersContacts(user_id=user_obj.id, contact_id=contact_obj.id)
        self.session.add(new_contact)
        self.session.commit()

    # Функция удаляет контакт из базы данных
    def remove_contact(self, user, contact):
        user_obj = self.session.query(AllUsers).filter_by(name=user).first()
        contact_obj = self.session.query(AllUsers).filter_by(name=contact).first()

        if not contact_obj:
            return

        self.session.query(UsersContacts).filter_by(user_id=user_obj.id, contact_id=contact_obj.id).delete()
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

    # Функция возвращает список контактов пользователя
    def get_contacts(self, username):
        user = self.session.query(AllUsers).filter_by(name=username).first()
        contacts = self.session.query(AllUsers.name).join(UsersContacts.contact).filter(
            UsersContacts.user_id == user.id
        )
        return [contact[0] for contact in contacts]

    # Функция возвращает историю действий пользователя
    def message_history(self):
        query = self.session.query(AllUsers.name, AllUsers.last_login, UsersHistory.sent, UsersHistory.accepted). \
            join(UsersHistory.user)
        return query


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
