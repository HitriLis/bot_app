"""Migrations message

Revision ID: a8bf638c0eda
Revises: 
Create Date: 2022-01-25 13:48:12.355441

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8bf638c0eda'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('with_bot', sa.Boolean(), nullable=True),
    sa.Column('bot_script', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    # ### end Alembic commands ###