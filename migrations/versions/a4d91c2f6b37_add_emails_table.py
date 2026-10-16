"""Add emails table

Revision ID: a4d91c2f6b37
Revises: 01838cff7e58
Create Date: 2026-10-16
"""
from alembic import op
import sqlalchemy as sa


revision = 'a4d91c2f6b37'
down_revision = '01838cff7e58'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'emails',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('remetente', sa.JSON(), nullable=False),
        sa.Column('destinatario', sa.JSON(), nullable=False),
        sa.Column('assunto', sa.String(length=100), nullable=False),
        sa.Column('texto', sa.String(length=500), nullable=False),
        sa.Column('dataHora', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('emails')
