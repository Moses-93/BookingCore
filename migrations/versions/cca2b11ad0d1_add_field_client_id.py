"""add field 'client_id'

Revision ID: cca2b11ad0d1
Revises: 5f88b99ceda4
Create Date: 2025-03-06 11:45:01.275157

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cca2b11ad0d1"
down_revision: Union[str, None] = "5f88b99ceda4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("business_info", sa.Column("client_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        None, "business_info", "users", ["client_id"], ["id"], ondelete="CASCADE"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "business_info", type_="foreignkey")
    op.drop_column("business_info", "client_id")
    # ### end Alembic commands ###
