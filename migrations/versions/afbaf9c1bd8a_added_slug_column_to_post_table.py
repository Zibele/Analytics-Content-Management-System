"""Added slug column to Post table

Revision ID: afbaf9c1bd8a
Revises: 7d82a6c99578
Create Date: 2018-08-20 14:11:09.933947

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'afbaf9c1bd8a'
down_revision = '7d82a6c99578'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('slug', sa.Text(), nullable=True))
    op.create_index(op.f('ix_post_slug'), 'post', ['slug'], unique=False)
    op.drop_column('post', 'subtitle')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('subtitle', sa.VARCHAR(length=128), nullable=True))
    op.drop_index(op.f('ix_post_slug'), table_name='post')
    op.drop_column('post', 'slug')
    # ### end Alembic commands ###
