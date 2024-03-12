"""Add stastashes

Revision ID: d8e631f799ab
Revises: 5c9b1a72ba07
Create Date: 2024-03-12 20:13:07.735936

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8e631f799ab'
down_revision: Union[str, None] = '5c9b1a72ba07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stash_items', sa.Column('chance_multiplayer', sa.Float(), nullable=False), schema='game')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stash_items', 'chance_multiplayer', schema='game')
    # ### end Alembic commands ###
