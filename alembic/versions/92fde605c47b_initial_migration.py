"""Initial migration

Revision ID: 92fde605c47b
Revises: 45bdd39177d2
Create Date: 2024-10-24 12:10:48.505439

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '92fde605c47b'
down_revision: Union[str, None] = '45bdd39177d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('auto_reply_enabled', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('reply_time', sa.Interval(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'reply_time')
    op.drop_column('users', 'auto_reply_enabled')
    # ### end Alembic commands ###
