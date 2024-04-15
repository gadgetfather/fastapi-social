"""add foreign key

Revision ID: 6154b837ea92
Revises: 67b209ac9f47
Create Date: 2024-04-14 12:03:59.140495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6154b837ea92'
down_revision: Union[str, None] = '67b209ac9f47'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'owner_id')
    pass
