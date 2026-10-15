import sqlite3
import json
import shutil
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("EnterpriseLocalServer")

def init_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE students (
        id INTEGER PRIMARY KEY,
        name TEXT,
        major TEXT,
        gpa REAL,
        award TEXT
    )
""")
    cursor.executemany("""
        INSERT INTO students (name, major, gpa, award) VALUES (?, ?, ?, ?)
""", [
    ("小李", "软件工程", 3.92, "特等奖学金"),
    ("小王", "人工智能", 3.75, "一等奖学金"),
    ("小张", "计算机科学", 3.60, "二等奖学金")
    ])
    conn.commit()
    return conn

db_conn = init_db()

@mcp.tool()
def query_database(sql: str) -> str:
    """
    在本地企业数据库执行 SQL 查询语句。
    数据表为 students，包含字段：id，name，major，gpa，award。
    示例：SELECT * FROM students WHERE name = '小李'
    """
    try:
        cursor = db_conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in rows]
        return json.dumps(results, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"SQL 执行失败: {str(e)}"})

@mcp.tool()
def check_disk_space() -> str:
    """
    检查当前服务器的硬盘存储健康度和剩余空间。
    """
    total, used, free = shutil.disk_usage("/")
    return json.dumps({
        "total_gb": round(total/ (2**30), 2),
        "used_gb": round(used/ (2**30), 2),
        "free_gb": round(free/ (2**30), 2)
    }, ensure_ascii=False)

if __name__ =="__main__":
    mcp.run(transport="stdio")