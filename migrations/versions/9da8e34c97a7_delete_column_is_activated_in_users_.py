"""delete column is_activated in users model

Revision ID: 9da8e34c97a7
Revises: e5fc1d70a028
Create Date: 2023-02-10 22:37:17.506756

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "9da8e34c97a7"
down_revision = "e5fc1d70a028"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "is_activated")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column("is_activated", sa.BOOLEAN(), server_default=sa.text("false"), autoincrement=False, nullable=True),
    )
    # ### end Alembic commands ###
