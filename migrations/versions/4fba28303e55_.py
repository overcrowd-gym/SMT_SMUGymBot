"""empty message

Revision ID: 4fba28303e55
Revises: 167e5b31ca3c
Create Date: 2020-03-18 17:39:58.646275

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4fba28303e55'
down_revision = '167e5b31ca3c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('visitorship', 'modified_timestamp')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('visitorship', sa.Column('modified_timestamp', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
