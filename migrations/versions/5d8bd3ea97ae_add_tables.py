"""add tables

Revision ID: 5d8bd3ea97ae
Revises: 
Create Date: 2022-11-26 14:33:43.798194

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '5d8bd3ea97ae'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('boards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('board_id', sa.Integer(), nullable=True),
    sa.Column('ordering', sa.Integer(), server_default='0', nullable=False),
    sa.ForeignKeyConstraint(['board_id'], ['boards.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('board_id', 'ordering', name='boards_ordering_uc')
    )
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('list_id', sa.Integer(), nullable=True),
    sa.Column('ordering', sa.Integer(), server_default='0', nullable=False),
    sa.ForeignKeyConstraint(['list_id'], ['lists.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('list_id', 'ordering', name='lists_ordering_uc')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks')
    op.drop_table('lists')
    op.drop_table('boards')
    op.drop_table('users')
    # ### end Alembic commands ###
