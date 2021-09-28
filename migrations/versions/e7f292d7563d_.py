"""empty message

Revision ID: e7f292d7563d
Revises: 3dab081f9dc6
Create Date: 2021-09-27 23:36:46.654044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7f292d7563d'
down_revision = '3dab081f9dc6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('roles_user_id_fkey', 'roles', type_='foreignkey')
    op.create_foreign_key(None, 'roles', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'roles', type_='foreignkey')
    op.create_foreign_key('roles_user_id_fkey', 'roles', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###