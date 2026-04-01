"""add timed workout set support

Revision ID: 20260401_0002
Revises: 20260330_0001
Create Date: 2026-04-01 23:59:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260401_0002"
down_revision = "20260330_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("workout_exercises", sa.Column("duration_seconds", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("workout_exercises", "duration_seconds")
