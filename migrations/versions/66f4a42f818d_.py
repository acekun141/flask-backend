"""empty message

Revision ID: 66f4a42f818d
Revises: 
Create Date: 2020-04-07 10:58:52.724317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66f4a42f818d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=60), nullable=False),
    sa.Column('last_name', sa.String(length=60), nullable=False),
    sa.Column('phonenumber', sa.String(length=20), nullable=True),
    sa.Column('address', sa.String(length=200), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_info_address'), 'user_info', ['address'], unique=False)
    op.create_index(op.f('ix_user_info_first_name'), 'user_info', ['first_name'], unique=False)
    op.create_index(op.f('ix_user_info_last_name'), 'user_info', ['last_name'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.String(), nullable=False),
    sa.Column('username', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=120), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_password_hash'), 'users', ['password_hash'], unique=False)
    op.create_index(op.f('ix_users_public_id'), 'users', ['public_id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_public_id'), table_name='users')
    op.drop_index(op.f('ix_users_password_hash'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_user_info_last_name'), table_name='user_info')
    op.drop_index(op.f('ix_user_info_first_name'), table_name='user_info')
    op.drop_index(op.f('ix_user_info_address'), table_name='user_info')
    op.drop_table('user_info')
    # ### end Alembic commands ###
