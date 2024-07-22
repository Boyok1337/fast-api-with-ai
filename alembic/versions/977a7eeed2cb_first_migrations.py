"""first migrations

Revision ID: 977a7eeed2cb
Revises: c4acbcd3c4dd
Create Date: 2024-07-22 15:57:55.446506

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "977a7eeed2cb"
down_revision: Union[str, None] = "c4acbcd3c4dd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
