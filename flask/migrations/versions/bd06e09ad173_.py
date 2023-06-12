"""empty message

Revision ID: bd06e09ad173
Revises: 
Create Date: 2022-06-03 11:02:32.184455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd06e09ad173'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attack',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('destination', sa.String(length=20), nullable=True),
    sa.Column('attacktype', sa.String(length=20), nullable=True),
    sa.Column('attacknum', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('blowup',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('url', sa.String(length=20), nullable=True),
    sa.Column('dictionary', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ipscan',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('IPs', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('portscan',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('IP', sa.String(length=20), nullable=True),
    sa.Column('port', sa.String(length=100), nullable=True),
    sa.Column('argument', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.Column('phonenumber', sa.String(length=11), nullable=True),
    sa.Column('email', sa.String(length=20), nullable=True),
    sa.Column('role', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('attackresult',
    sa.Column('result_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('destination', sa.String(length=20), nullable=True),
    sa.Column('attacknum', sa.Integer(), nullable=True),
    sa.Column('attacktype', sa.String(length=20), nullable=True),
    sa.Column('result', sa.String(length=20), nullable=True),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['attack.id'], ),
    sa.PrimaryKeyConstraint('result_id')
    )
    op.create_table('blowupresult',
    sa.Column('result_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('url', sa.String(length=20), nullable=True),
    sa.Column('subdomain', sa.String(length=100), nullable=True),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['blowup.id'], ),
    sa.PrimaryKeyConstraint('result_id')
    )
    op.create_table('ipscanresult',
    sa.Column('result_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ip', sa.String(length=20), nullable=True),
    sa.Column('mac', sa.String(length=20), nullable=True),
    sa.Column('state', sa.String(length=20), nullable=True),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['ipscan.id'], ),
    sa.PrimaryKeyConstraint('result_id')
    )
    op.create_table('portscanresult',
    sa.Column('result_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('host', sa.String(length=20), nullable=True),
    sa.Column('protocol', sa.String(length=20), nullable=True),
    sa.Column('port', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('state', sa.String(length=20), nullable=True),
    sa.Column('reason', sa.String(length=20), nullable=True),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['portscan.id'], ),
    sa.PrimaryKeyConstraint('result_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('portscanresult')
    op.drop_table('ipscanresult')
    op.drop_table('blowupresult')
    op.drop_table('attackresult')
    op.drop_table('users')
    op.drop_table('portscan')
    op.drop_table('ipscan')
    op.drop_table('blowup')
    op.drop_table('attack')
    # ### end Alembic commands ###
