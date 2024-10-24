"""Initial migration

Revision ID: 7bc589bf256e
Revises: f3be8d23a81f
Create Date: 2024-10-23 23:29:38.310933

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7bc589bf256e'
down_revision: Union[str, None] = 'f3be8d23a81f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('is_banned', sa.Boolean(), nullable=True))
    op.add_column('posts', sa.Column('is_banned', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'is_banned')
    op.drop_column('comments', 'is_banned')
    # ### end Alembic commands ###
