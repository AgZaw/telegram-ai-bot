from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

Base = declarative_base()

class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50))
    role = Column(String(20))
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class AgentState(Base):
    __tablename__ = 'agent_state'
    id = Column(Integer, primary_key=True)
    system_prompt = Column(Text)
    version = Column(Integer, default=1)

engine = create_engine('sqlite:///agent_data.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def save_message(user_id, role, content):
    session = Session()
    try:
        msg = Conversation(user_id=str(user_id), role=role, content=content)
        session.add(msg)
        session.commit()
    finally:
        session.close()

def get_history(user_id, limit=10):
    session = Session()
    try:
        history = session.query(Conversation).filter_by(user_id=str(user_id)).order_by(Conversation.timestamp.desc()).limit(limit).all()
        return [{"role": h.role, "content": h.content} for h in reversed(history)]
    finally:
        session.close()

def update_system_prompt(new_prompt):
    session = Session()
    try:
        state = session.query(AgentState).first()
        if not state:
            state = AgentState(system_prompt=new_prompt)
            session.add(state)
        else:
            state.system_prompt = new_prompt
            state.version += 1
        session.commit()
    finally:
        session.close()

def get_system_prompt():
    session = Session()
    try:
        state = session.query(AgentState).first()
        if state:
            return state.system_prompt
        return "You are a self-learning AI agent. Help users and learn from interactions."
    finally:
        session.close()
