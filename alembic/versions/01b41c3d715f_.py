"""empty message

Revision ID: 01b41c3d715f
Revises: 99ec2ee9645b
Create Date: 2024-11-22 10:20:30.125506

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '01b41c3d715f'
down_revision: Union[str, None] = '99ec2ee9645b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=False))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat', schema=None) as batch_op:
        batch_op.drop_column('title')

    # ### end Alembic commands ###
