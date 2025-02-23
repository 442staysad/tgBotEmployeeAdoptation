from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TGBotAdminCategory(Base):
    __tablename__ = 'TGBotAdmin_category'

    id = Column(Integer, primary_key=True)
    CategoryName = Column(String)
    CategoryAnswer = Column(String)

class TGBotAdminQuestion(Base):
    __tablename__ = 'TGBotAdmin_question'

    id = Column(Integer, primary_key=True)
    QuestionText = Column(String)
    QuestionAnswer = Column(String)
    CategoryID = Column(Integer)

class DataService:
    def __init__(self):
        # создаем подключение к базе данных
        engine = create_engine('sqlite:///tgbotdb.db')
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_categories(self):
        # получаем категории из базы данных
        return self.session.query(TGBotAdminCategory).all()

    def get_question_answer(self, question):
        # получаем ответ на вопрос из базы данных
        question_obj = self.session.query(TGBotAdminQuestion).filter_by(QuestionText=question).first()
        return question_obj.QuestionAnswer if question_obj else None

    def get_questions_by_category(self, category):
        # получаем вопросы по категории из базы данных
        category_obj = self.session.query(TGBotAdminCategory).filter_by(CategoryName=category).first()
        if not category_obj:
            return []
        questions = self.session.query(TGBotAdminQuestion).filter_by(CategoryID=category_obj.id).all()
        return [question.QuestionText for question in questions]

    def get_category_answer(self, category):
        # получаем ответ на категорию из базы данных
        category_obj = self.session.query(TGBotAdminCategory).filter_by(CategoryName=category).first()
        return category_obj.CategoryAnswer if category_obj else None

    def get_questions_count_by_category(self, category):
        # получаем количество вопросов в категории из базы данных
        category_obj = self.session.query(TGBotAdminCategory).filter_by(CategoryName=category).first()
        if not category_obj:
            return 0
        questions_count = self.session.query(TGBotAdminQuestion).filter_by(CategoryID=category_obj.id).count()
        return questions_count
