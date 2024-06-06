"""begin

Revision ID: e030bfe8aeb6
Revises: 
Create Date: 2024-06-06 15:22:05.957451

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e030bfe8aeb6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Bots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('database', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('middle_name', sa.String(), nullable=False),
    sa.Column('surname', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('RefreshSessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('token_hash', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('expires_in', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('ip_address', sa.String(), nullable=False),
    sa.Column('user_agent', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('UserBots',
    sa.Column('UserId', sa.Integer(), nullable=True),
    sa.Column('BotId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['BotId'], ['Bots.id'], ),
    sa.ForeignKeyConstraint(['UserId'], ['Users.id'], )
    )
    op.create_table('UserRoles',
    sa.Column('UserId', sa.Integer(), nullable=True),
    sa.Column('RoleId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['RoleId'], ['Roles.id'], ),
    sa.ForeignKeyConstraint(['UserId'], ['Users.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('UserRoles')
    op.drop_table('UserBots')
    op.drop_table('RefreshSessions')
    op.drop_table('Users')
    op.drop_table('Roles')
    op.drop_table('Bots')
    # ### end Alembic commands ###