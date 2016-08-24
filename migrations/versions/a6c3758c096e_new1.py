"""new1

Revision ID: a6c3758c096e
Revises: 9b45cca44510
Create Date: 2016-08-20 23:56:56.252862

"""

# revision identifiers, used by Alembic.
revision = 'a6c3758c096e'
down_revision = '9b45cca44510'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tag', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('likes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('like_sum', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('articles', sa.Column('item_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_articles_title'), 'articles', ['title'], unique=False)
    op.drop_constraint(None, 'articles', type_='foreignkey')
    op.create_foreign_key(None, 'articles', 'items', ['item_id'], ['id'])
    op.drop_column('articles', 'author_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('articles', sa.Column('author_id', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'articles', type_='foreignkey')
    op.create_foreign_key(None, 'articles', 'users', ['author_id'], ['id'])
    op.drop_index(op.f('ix_articles_title'), table_name='articles')
    op.drop_column('articles', 'item_id')
    op.drop_table('likes')
    op.drop_table('items')
    ### end Alembic commands ###