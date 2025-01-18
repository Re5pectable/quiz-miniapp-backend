from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class QuizOrm(Base):
    __tablename__ = "quizes"
    id = sa.Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = sa.Column(sa.DateTime(), server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime(), onupdate=sa.func.now())
    type = sa.Column(sa.String())
    header = sa.Column(sa.String())
    short_name = sa.Column(sa.String())
    text = sa.Column(sa.String())
    config = sa.Column(postgresql.JSONB())
    point_fields = sa.Column(postgresql.JSONB())
    logo_url = sa.Column(sa.String())


class QuizQuestionOrm(Base):
    __tablename__ = "quiz_questions"
    id = sa.Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = sa.Column(sa.DateTime(), server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime(), onupdate=sa.func.now())
    quiz_id = sa.Column(postgresql.UUID(as_uuid=True), sa.ForeignKey("quizes.id"), index=True)
    text = sa.Column(sa.String())
    pic_url = sa.Column(sa.String())
    order = sa.Column(sa.Integer())


class QuizQuestionsAnswer(Base):
    __tablename__ = "quiz_question_answers"
    id = sa.Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = sa.Column(sa.DateTime(), server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime(), onupdate=sa.func.now())
    quiz_question_id = sa.Column(postgresql.UUID(as_uuid=True), sa.ForeignKey("quiz_questions.id"), index=True)
    text = sa.Column(sa.String())
    note = sa.Column(sa.String())
    points = sa.Column(sa.String())
    order = sa.Column(sa.Integer())


class QuizResultOrm(Base):
    __tablename__ = "quiz_results"
    id = sa.Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = sa.Column(sa.DateTime(), server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime(), onupdate=sa.func.now())
    quiz_id = sa.Column(postgresql.UUID(as_uuid=True), sa.ForeignKey("quizes.id"), index=True)
    header = sa.Column(sa.String())
    text = sa.Column(sa.String())
    points = sa.Column(postgresql.JSONB())
    pic_url = sa.Column(sa.String())


class GameOrm(Base):
    __tablename__ = "games"
    id = sa.Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = sa.Column(sa.DateTime(), server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime(), onupdate=sa.func.now())
    quiz_id = sa.Column(postgresql.UUID(as_uuid=True), sa.ForeignKey("quizes.id"), index=True)
    status = sa.Column(sa.String())


class GameAnswerOrm(Base):
    __tablename__ = "game_answers"
    id = sa.Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = sa.Column(sa.DateTime(), server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime(), onupdate=sa.func.now())
    game_id = sa.Column(postgresql.UUID(as_uuid=True), sa.ForeignKey("games.id"), index=True)
    quiz_answer_id = sa.Column(postgresql.UUID(as_uuid=True), sa.ForeignKey("quiz_question_answers.id"))


class GameResultOrm(Base):
    __tablename__ = "game_results"
    id = sa.Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = sa.Column(sa.DateTime(), server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime(), onupdate=sa.func.now())
    game_id = sa.Column(postgresql.UUID(as_uuid=True), sa.ForeignKey("games.id"), index=True)
    quiz_result_id = sa.Column(postgresql.UUID(as_uuid=True), sa.ForeignKey("quiz_results.id"), index=True)
    quiz_result_copy = sa.Column(postgresql.JSONB())


class InvitationOrm(Base):
    __tablename__ = "invitations"
    id = sa.Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = sa.Column(sa.DateTime(), server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime(), onupdate=sa.func.now())
    short_name = sa.Column(sa.String(), index=True)
    game_result_id = sa.Column(postgresql.UUID(as_uuid=True), sa.ForeignKey("game_results.id"), index=True)
    game_result_copy = sa.Column(postgresql.JSONB())
    click_counter = sa.Column(sa.Integer())
