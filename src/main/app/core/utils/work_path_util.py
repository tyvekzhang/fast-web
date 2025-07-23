"""Work path operation util"""

import os

current_dir: str = os.path.dirname(os.path.abspath(__file__))
resource_dir: str = os.path.abspath(
    os.path.join(current_dir, os.pardir, os.pardir, os.pardir, "resource")
)
db_path = os.path.join(resource_dir, "alembic/db/df.db")
