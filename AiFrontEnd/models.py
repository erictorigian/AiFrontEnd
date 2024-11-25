import reflex as rx
import sqlalchemy as sa
from datetime import datetime, timezone
from sqlmodel import Field, Relationship
from typing import List

def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)

class ChatSession(rx.Model, table=True):
    #title: str
    messages: List['ChatSessionMessageModel'] = Relationship(back_populates='session')
    created_at: datetime = Field(
        default_factory= get_utc_now,
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs= {
            'server_default': sa.func.now()
        },
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory= get_utc_now,
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs= {
            'server_default': sa.func.now()
        },
        nullable=False
    )
    
class ChatSessionMessageModel(rx.Model, table=True):
    session_id: int = Field(default=None, foreign_key="chatsession.id")
    session: ChatSession = Relationship(back_populates="messages")
    role: str
    content: str
    created_at: datetime = Field(
        default_factory= get_utc_now,
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs= {
            'server_default': sa.func.now()
        },
        nullable=False
    )
    