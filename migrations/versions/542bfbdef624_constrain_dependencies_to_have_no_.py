"""Constrain dependencies to have no duplicates. Uses new JSON serialization/deserialization
(serde) to consistently store the dependency bindings.

Revision ID: 542bfbdef624
Revises: 99fd5e88689c
Create Date: 2022-09-13 10:57:44.977492

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.orm import sessionmaker

from buildingmotif.database.tables import DepsAssociation

# revision identifiers, used by Alembic.
revision = "542bfbdef624"
down_revision = "99fd5e88689c"
branch_labels = None
depends_on = None


def upgrade():
    # add NULLABLE 'id' column
    with op.batch_alter_table("deps_association_table", schema=None) as batch_op:
        batch_op.drop_constraint("deps_association_table_pkey", type_="primary")
        batch_op.add_column(sa.Column("id", sa.Integer(), primary_key=True))

        batch_op.alter_column(
            "dependant_id", existing_type=sa.INTEGER(), nullable=False
        )
        batch_op.alter_column("dependee_id", existing_type=sa.INTEGER(), nullable=False)
        batch_op.create_unique_constraint(
            "deps_association_unique_constraint",
            ["dependant_id", "dependee_id", "args"],
        )

    # now that 'id' exists, update the serde of the deps field by copying all the deps
    # out and then putting them back in
    conn = op.get_bind()
    Session = sessionmaker()
    with Session(bind=conn) as session:
        deps = session.query(DepsAssociation).all()
        for dep in deps:
            args = dep.args.copy()
            dep.args = [(k, v) for k, v in args.items()]
            session.add(dep)
        session.commit()


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("template", schema=None) as batch_op:
        batch_op.create_index("ix_template_name", ["name"], unique=False)

    with op.batch_alter_table("deps_association_table", schema=None) as batch_op:
        batch_op.drop_constraint("deps_association_unique_constraint", type_="unique")
        batch_op.alter_column("dependee_id", existing_type=sa.INTEGER(), nullable=False)
        batch_op.alter_column(
            "dependant_id", existing_type=sa.INTEGER(), nullable=False
        )
        batch_op.drop_column("id")

    # ### end Alembic commands ###
