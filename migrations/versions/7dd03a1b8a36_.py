"""empty message

Revision ID: 7dd03a1b8a36
Revises: f0c224fceba2
Create Date: 2021-07-07 22:06:17.346693

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7dd03a1b8a36'
down_revision = 'f0c224fceba2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('detections', sa.Column('detection', sa.String(length=160), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('detections', 'detection')
    # ### end Alembic commands ###
