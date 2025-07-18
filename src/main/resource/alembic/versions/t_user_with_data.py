"""empty message

Revision ID: b1b9afcafd1a
Revises:
Create Date: 2025-03-06 23:02:06.630914

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "b1b9afcafd1a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "sys_user",
        sa.Column("id", sa.BigInteger(), nullable=False, comment="主键"),
        sa.Column(
            "username", sa.String(length=32), nullable=False, comment="用户名"
        ),
        sa.Column(
            "password", sa.String(length=64), nullable=False, comment="密码"
        ),
        sa.Column(
            "nickname", sa.String(length=32), nullable=False, comment="昵称"
        ),
        sa.Column(
            "avatar_url",
            sa.String(length=64),
            nullable=True,
            comment="头像地址",
        ),
        sa.Column(
            "status",
            sa.Integer(),
            nullable=True,
            comment="状态(0:停用,1:待审核,2:正常,3:已注销)",
        ),
        sa.Column(
            "remark", sa.String(length=255), nullable=True, comment="备注"
        ),
        sa.Column(
            "create_time", sa.DateTime(), nullable=True, comment="创建时间"
        ),
        sa.Column(
            "update_time", sa.DateTime(), nullable=True, comment="更新时间"
        ),
        sa.PrimaryKeyConstraint("id"),
        comment="用户信息表",
    )
    op.create_index(
        op.f("ix_sys_user_username"), "sys_user", ["username"], unique=True
    )
    op.execute("""
        INSERT INTO sys_user (id, username, password, nickname, avatar_url, status, remark, create_time, update_time) VALUES(9, 'admin', '$2b$12$qupycbom77r6MoRuCW5L8um0QUmCazQgBNfv4otYwX3nnXP55dVg6', '管理员', NULL, 1, '管理员', '2025-05-21 22:18:22.868513', '2025-05-21 22:18:22.868513');
    """)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_sys_user_username"), table_name="sys_user")
    op.drop_table("sys_user")
    # ### end Alembic commands ###
