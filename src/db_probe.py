from __future__ import annotations

import argparse
from pathlib import Path
import yaml
import pymysql

CFG_PATH = Path("config/database.yaml")

def load_cfg(profile: str) -> dict:
    if not CFG_PATH.exists():
        raise SystemExit("Missing config/database.yaml")

    cfg_all = yaml.safe_load(CFG_PATH.read_text())
    if profile not in cfg_all:
        raise SystemExit(f"Profile '{profile}' not found in config/database.yaml")

    return cfg_all[profile]

def connect(cfg: dict):
    return pymysql.connect(
        host=cfg["host"],
        port=int(cfg["port"]),
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )

def fetch_tables(conn) -> list[str]:
    sql = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = DATABASE()
    ORDER BY table_name
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
    return [r["table_name"] for r in rows]

def sample_table(conn, table: str, limit: int = 20) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM `{table}` LIMIT {limit}")
        return cur.fetchall()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile",
        required=True,
        help="Database profile name in config/database.yaml (e.g. tonglian, juyuan)",
    )
    args = parser.parse_args()

    cfg = load_cfg(args.profile)
    conn = connect(cfg)

    try:
        tables = fetch_tables(conn)
        print(f"[{args.profile}] Total tables: {len(tables)}")
        print("Tables (first 50):")
        for t in tables[:50]:
            print(t)

        if not tables:
            print("No tables found.")
            return

        t0 = tables[0]
        print(f"\nSample from `{t0}` (LIMIT 20):")
        rows = sample_table(conn, t0, limit=20)
        if not rows:
            print("(no rows)")
            return

        keys = list(rows[0].keys())
        print("Columns:", keys)
        for r in rows[:5]:
            print(r)

    finally:
        conn.close()

if __name__ == "__main__":
    main()
