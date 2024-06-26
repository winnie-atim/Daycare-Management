"""change of time datatype

Revision ID: aff3796c481f
Revises: 9d044c0b0614
Create Date: 2024-05-12 00:43:13.488466

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'aff3796c481f'
down_revision: Union[str, None] = '9d044c0b0614'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('baby', 'time_of_arrival',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.Time(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('baby', 'time_of_arrival',
               existing_type=sa.Time(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)
    # ### end Alembic commands ###
