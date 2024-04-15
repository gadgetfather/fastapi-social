"""modify posts

Revision ID: 68664d26b594
Revises: b77cc48b30c3
Create Date: 2024-04-14 11:57:08.843837

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68664d26b594'
down_revision: Union[str, None] = 'b77cc48b30c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'owner_id')
    pass
