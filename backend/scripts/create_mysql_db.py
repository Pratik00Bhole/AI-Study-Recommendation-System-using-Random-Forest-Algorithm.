import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url


def main() -> int:
    database_url = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:lotus@127.0.0.1:3306/ai_study_recommendation",
    )

    try:
        url = make_url(database_url)
    except Exception as exc:
        print(f"Invalid DATABASE_URL: {exc}")
        return 1

    if not str(url.drivername).startswith("mysql"):
        print("DATABASE_URL must use a MySQL driver, e.g. mysql+pymysql://...")
        return 1

    target_db = url.database
    if not target_db:
        print("DATABASE_URL must include a database name")
        return 1

    admin_url = url.set(database="mysql")

    try:
        engine = create_engine(admin_url, pool_pre_ping=True)
        with engine.connect() as connection:
            connection.execute(
                text(
                    f"CREATE DATABASE IF NOT EXISTS `{target_db}` "
                    "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                )
            )
            connection.commit()

        verify_engine = create_engine(url, pool_pre_ping=True)
        with verify_engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        print(f"Database ready: {target_db}")
        return 0
    except Exception as exc:
        print(f"Failed to create/verify database '{target_db}': {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
