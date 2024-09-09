"""Add content column into posts table

Revision ID: 0b97e61091d6
Revises: ba2734a30549
Create Date: 2024-03-10 10:33:16.773305

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b97e61091d6'
down_revision: Union[str, None] = 'ba2734a30549'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
