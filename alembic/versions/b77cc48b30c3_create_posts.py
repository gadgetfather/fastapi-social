"""create posts

Revision ID: b77cc48b30c3
Revises: 
Create Date: 2024-04-14 11:53:11.130830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b77cc48b30c3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('title', sa.String),
        sa.Column('content', sa.String),
        sa.Column('published', sa.Boolean)
    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
