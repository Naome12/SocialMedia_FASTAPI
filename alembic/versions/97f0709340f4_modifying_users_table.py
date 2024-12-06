"""modifying users table

Revision ID: 97f0709340f4
Revises: 539881f7c311
Create Date: 2024-11-12 13:50:34.695324

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97f0709340f4'
down_revision: Union[str, None] = '539881f7c311'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('Dob', sa.Date(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'Dob')
    # ### end Alembic commands ###