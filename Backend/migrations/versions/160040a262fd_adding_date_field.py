"""adding date field

Revision ID: 160040a262fd
Revises: 8e35c601df46
Create Date: 2024-05-18 20:28:02.733083

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '160040a262fd'
down_revision: Union[str, None] = '8e35c601df46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
