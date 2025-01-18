"""Init

Revision ID: 56aa2a2ce437
Revises: 
Create Date: 2025-01-06 13:06:52.668713

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "56aa2a2ce437"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "dates",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("free", sa.Boolean(), nullable=True),
        sa.Column("del_time", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_dates_free"), "dates", ["free"], unique=False)
    op.create_table(
        "services",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("duration", sa.Interval(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("chat_id", sa.Integer(), nullable=False),
        sa.Column("admin", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_chat_id"), "users", ["chat_id"], unique=True)
    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=True),
        sa.Column("time", sa.Time(), nullable=False),
        sa.Column("reminder_hours", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("name_id", sa.Integer(), nullable=True),
        sa.Column("service_id", sa.Integer(), nullable=True),
        sa.Column("date_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["date_id"], ["dates.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["name_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["service_id"], ["services.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_bookings_active"), "bookings", ["active"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_bookings_active"), table_name="bookings")
    op.drop_table("bookings")
    op.drop_index(op.f("ix_users_chat_id"), table_name="users")
    op.drop_table("users")
    op.drop_table("services")
    op.drop_index(op.f("ix_dates_free"), table_name="dates")
    op.drop_table("dates")
    # ### end Alembic commands ###
