"""add Auto_vote

Revision ID: d278da0fa679
Revises: db14dad9c30a
Create Date: 2024-03-10 11:28:26.101645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd278da0fa679'
down_revision: Union[str, None] = 'db14dad9c30a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('votes',
                    sa.Column('user_id',sa.Integer(),nullable=False),
                    sa.Column('post_id',sa.Integer(),nullable=False),
                    sa.ForeignKeyConstraint(['post_id'],['posts.id'],ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'],['users.id'],ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('user_id','post_id'))
def downgrade() -> None:
    op.drop_table('votes')
    pass
