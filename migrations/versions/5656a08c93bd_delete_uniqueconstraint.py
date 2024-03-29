"""delete UniqueConstraint

Revision ID: 5656a08c93bd
Revises: 7ebbf5d8b55b
Create Date: 2023-02-11 23:22:14.338859

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "5656a08c93bd"
down_revision = "7ebbf5d8b55b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("boards_ordering_uc", "lists", type_="unique")
    op.drop_constraint("lists_ordering_uc", "tasks", type_="unique")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint("lists_ordering_uc", "tasks", ["list_id", "ordering"])
    op.create_unique_constraint("boards_ordering_uc", "lists", ["board_id", "ordering"])
    # ### end Alembic commands ###
