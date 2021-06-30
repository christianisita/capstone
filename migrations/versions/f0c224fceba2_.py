"""empty message

Revision ID: f0c224fceba2
Revises: 1c29bed70ad5
Create Date: 2021-06-30 09:36:39.055106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0c224fceba2'
down_revision = '1c29bed70ad5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'detections', ['id'])
    op.add_column('patients', sa.Column('patient_number', sa.String(length=20), nullable=False))
    op.drop_constraint('patients_nik_key', 'patients', type_='unique')
    op.create_unique_constraint(None, 'patients', ['id'])
    op.create_unique_constraint(None, 'patients', ['patient_number'])
    op.drop_column('patients', 'nik')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('patients', sa.Column('nik', sa.VARCHAR(length=20), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'patients', type_='unique')
    op.drop_constraint(None, 'patients', type_='unique')
    op.create_unique_constraint('patients_nik_key', 'patients', ['nik'])
    op.drop_column('patients', 'patient_number')
    op.drop_constraint(None, 'detections', type_='unique')
    # ### end Alembic commands ###