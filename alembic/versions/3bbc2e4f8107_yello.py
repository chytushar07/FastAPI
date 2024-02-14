"""yello

Revision ID: 3bbc2e4f8107
Revises: 
Create Date: 2024-02-12 12:28:56.724875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3bbc2e4f8107'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# To handle changes
def upgrade():
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )

# To handle rolling back
def downgrade():
    op.drop_table('account')
    pass
