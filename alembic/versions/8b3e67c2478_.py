"""empty message

Revision ID: 8b3e67c2478
Revises: b111ea8d507
Create Date: 2012-11-26 18:51:59.154000

"""

# revision identifiers, used by Alembic.
revision = '8b3e67c2478'
down_revision = 'b111ea8d507'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('companies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('incorp_type', sa.String(length=10), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['entities.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('judges',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['persons.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lawfirms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['companies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('litigation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=150), nullable=True),
    sa.Column('caseno', sa.String(length=20), nullable=True),
    sa.Column('court', sa.String(length=10), nullable=True),
    sa.Column('filed', sa.Date(), nullable=True),
    sa.Column('judge_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['judge_id'], ['judges.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('litigation_defendants',
    sa.Column('litigation_id', sa.Integer(), nullable=True),
    sa.Column('entity_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['entity_id'], ['entities.id'], ),
    sa.ForeignKeyConstraint(['litigation_id'], ['litigation.id'], ),
    sa.PrimaryKeyConstraint()
    )
    op.create_table('litigation_patents',
    sa.Column('litigation_id', sa.Integer(), nullable=True),
    sa.Column('patent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['litigation_id'], ['litigation.id'], ),
    sa.ForeignKeyConstraint(['patent_id'], ['patents.id'], ),
    sa.PrimaryKeyConstraint()
    )
    op.create_table('litigation_plaintiffs',
    sa.Column('litigation_id', sa.Integer(), nullable=True),
    sa.Column('entity_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['entity_id'], ['entities.id'], ),
    sa.ForeignKeyConstraint(['litigation_id'], ['litigation.id'], ),
    sa.PrimaryKeyConstraint()
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('litigation_plaintiffs')
    op.drop_table('litigation_patents')
    op.drop_table('litigation_defendants')
    op.drop_table('litigation')
    op.drop_table('lawfirms')
    op.drop_table('judges')
    op.drop_table('companies')
    ### end Alembic commands ###
