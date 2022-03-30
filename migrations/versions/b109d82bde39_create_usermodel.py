"""create userModel

Revision ID: b109d82bde39
Revises: 31014ba76381
Create Date: 2022-03-30 18:52:12.040036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b109d82bde39'
down_revision = '31014ba76381'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_model_username'), 'user_model', ['username'], unique=False)
    op.alter_column('author_model', 'surname',
               existing_type=sa.VARCHAR(length=32),
               nullable=False,
               existing_server_default=sa.text("('')"))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('author_model', 'surname',
               existing_type=sa.VARCHAR(length=32),
               nullable=True,
               existing_server_default=sa.text("('')"))
    op.drop_index(op.f('ix_user_model_username'), table_name='user_model')
    op.drop_table('user_model')
    # ### end Alembic commands ###
