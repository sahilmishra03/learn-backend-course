"""add new column

Revision ID: 3bda3a8e09ac
Revises: fab89ba1ad6a
Create Date: 2026-03-12 12:44:39.104028

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3bda3a8e09ac'
down_revision: Union[str, Sequence[str], None] = 'fab89ba1ad6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
