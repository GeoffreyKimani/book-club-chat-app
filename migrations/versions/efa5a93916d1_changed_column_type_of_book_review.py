"""Changed column type of book(review)

Revision ID: efa5a93916d1
Revises: 8d4d698a1770
Create Date: 2019-11-07 11:20:02.966291

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efa5a93916d1'
down_revision = '8d4d698a1770'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        table_name='book',
        column_name='review',
        nullable=True,
        existing_type=sa.VARCHAR(length=255),
        type_=sa.Text)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        table_name='book',
        column_name='review',
        nullable=True,
        existing_type=sa.Text,
        type_=sa.VARCHAR(length=255)
    )
    # ### end Alembic commands ###
