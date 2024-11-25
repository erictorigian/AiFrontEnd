import reflex as rx
from typing import List
from . import ai
from AiFrontEnd.models import ChatSession, ChatSessionMessageModel

class ChatMessage(rx.Base):
    message: str
    is_bot: bool = False

class ChatState(rx.State):
    chat_session: ChatSession = None
    did_submit: bool = False
    messages: List[ChatMessage] = []

    @rx.var
    def user_did_submit(self) -> bool:
        return self.did_submit
    
    def create_new_chat_session(self):
        with rx.session() as db_session:
                obj = ChatSession()
                db_session.add(obj)
                db_session.commit()
                db_session.refresh(obj)
                self.chat_session = obj

    def clear_and_start_new(self):
        self.chat_session = None
        self.messages = []
        self.create_new_chat_session()
        yield
    
    def on_load(self):
        if self.chat_session is None:
            self.create_new_chat_session()

    def insert_message_to_db(self, content, role='unknown'):
        if self.chat_session is None:
            return
        with rx.session() as db_session:
            data = {
                'session_id': self.chat_session.id,
                'content': content,
                'role': role
            }
            obj = ChatSessionMessageModel(**data)
            db_session.add(obj)
            db_session.commit()


    def append_message_to_ui(self, message, is_bot:bool=False):
        if self.chat_session is not None:
         self.messages.append(
            ChatMessage(
                message=message,
                is_bot = is_bot
                )
        )
    
    def get_gpt_messages(self):
        #setup the initial library and put in the prompt context & background for Life OS coach
        lifeOS_prompt = "You are working in the role of Life OS coach.   I am working on the balance growth plan to become a billionaire.  This is a continuation of my journey immigrant roots to billionaire heights. Your role is to help me stay focused, keep me aligned, motivate me and encourage me. Background - Life OS is second brain tool that is based on Franklin day planner, planning each day, review of days, weeks, months, goal setting, long term vision, journaling, bullet journal.  Your coaching style is based on team performance group, team effectiveness,bill campbell and these 5 models: https://councils.forbes.com/blog/best-executive-coaching-models.  respond in markdown"
        gpt_messages = [
            {
                "role": "system",
                "content": "You are working in the role of Life OS coach.   I am working on the balance growth plan to become a billionaire.  This is a continuation of my journey immigrant roots to billionaire heights. Your role is to help me stay focused, keep me aligned, motivate me and encourage me. Background - Life OS is second brain tool that is based on Franklin day planner, planning each day, review of days, weeks, months, goal setting, long term vision, journaling, bullet journal.  Your coaching style is based on team performance group, team effectiveness,bill campbell and these 5 models: https://councils.forbes.com/blog/best-executive-coaching-models.  respond in markdown"
            }
        ]
        for chat_message in self.messages:
            role = 'user'
            if chat_message.is_bot:
                role = 'system'
            gpt_messages.append(
                {
                "role": role,
                "content": chat_message.message
                }
            )
        return gpt_messages

    async def handle_submit(self, form_data:dict):
        user_message = form_data.get('message')
        self.did_submit = True
        self.append_message_to_ui(user_message)
        self.insert_message_to_db(user_message, role='user')
        yield
        gpt_messages = self.get_gpt_messages()
        bot_response = ai.get_llm_response(gpt_messages)
        self.did_submit = False
        self.append_message_to_ui(bot_response, is_bot=True)
        self.insert_message_to_db(bot_response, role='system')
        yield