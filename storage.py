"""
数据存储模块
使用 SQLite 进行持久化存储
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class StringStorage:
    """字符串存储管理器"""

    def __init__(self, db_path="data/strings.db"):
        self.db_path = db_path
        self._ensure_db_directory()
        self._init_database()

    def _ensure_db_directory(self):
        """确保数据库目录存在"""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)

    def _init_database(self):
        """初始化数据库表结构"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS strings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    value TEXT NOT NULL,
                    format TEXT NOT NULL,
                    length INTEGER,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            conn.commit()

    def save(self, name: str, value: str, format_type: str, length: Optional[int] = None) -> Dict:
        """
        保存字符串

        Args:
            name: 自定义名称（唯一）
            value: 字符串值
            format_type: 格式类型
            length: 长度（可选）

        Returns:
            保存的记录

        Raises:
            ValueError: 名称已存在
        """
        now = datetime.now().isoformat()

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    INSERT INTO strings (name, value, format, length, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (name, value, format_type, length, now, now))
                conn.commit()

                return {
                    "id": cursor.lastrowid,
                    "name": name,
                    "value": value,
                    "format": format_type,
                    "length": length,
                    "created_at": now,
                    "updated_at": now
                }
        except sqlite3.IntegrityError:
            raise ValueError(f"名称 '{name}' 已存在")

    def get_all(self, search: Optional[str] = None) -> List[Dict]:
        """
        获取所有字符串记录

        Args:
            search: 搜索关键词（可选，搜索名称和值）

        Returns:
            记录列表
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            if search:
                cursor = conn.execute("""
                    SELECT * FROM strings
                    WHERE name LIKE ? OR value LIKE ?
                    ORDER BY created_at DESC
                """, (f"%{search}%", f"%{search}%"))
            else:
                cursor = conn.execute("""
                    SELECT * FROM strings
                    ORDER BY created_at DESC
                """)

            return [dict(row) for row in cursor.fetchall()]

    def get_by_id(self, string_id: int) -> Optional[Dict]:
        """根据 ID 获取记录"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM strings WHERE id = ?", (string_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_by_name(self, name: str) -> Optional[Dict]:
        """根据名称获取记录"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM strings WHERE name = ?", (name,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update(self, string_id: int, name: Optional[str] = None, value: Optional[str] = None) -> bool:
        """
        更新记录

        Args:
            string_id: 记录 ID
            name: 新名称（可选）
            value: 新值（可选）

        Returns:
            是否更新成功
        """
        updates = []
        params = []

        if name is not None:
            updates.append("name = ?")
            params.append(name)

        if value is not None:
            updates.append("value = ?")
            params.append(value)

        if not updates:
            return False

        updates.append("updated_at = ?")
        params.append(datetime.now().isoformat())
        params.append(string_id)

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    f"UPDATE strings SET {', '.join(updates)} WHERE id = ?",
                    params
                )
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            raise ValueError(f"名称 '{name}' 已存在")

    def delete(self, string_id: int) -> bool:
        """
        删除记录

        Args:
            string_id: 记录 ID

        Returns:
            是否删除成功
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM strings WHERE id = ?", (string_id,))
            conn.commit()
            return cursor.rowcount > 0

    def export_json(self) -> str:
        """导出所有记录为 JSON 格式"""
        records = self.get_all()
        return json.dumps(records, ensure_ascii=False, indent=2)

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) as total FROM strings")
            total = cursor.fetchone()[0]

            cursor = conn.execute("""
                SELECT format, COUNT(*) as count
                FROM strings
                GROUP BY format
            """)
            by_format = {row[0]: row[1] for row in cursor.fetchall()}

            return {
                "total": total,
                "by_format": by_format
            }


if __name__ == "__main__":
    # 测试代码
    storage = StringStorage("data/test.db")

    print("=== 存储模块测试 ===\n")

    # 保存测试
    try:
        record = storage.save("test_key", "custom-abc123", "hex", 32)
        print(f"保存成功: {record}")
    except ValueError as e:
        print(f"保存失败: {e}")

    # 查询测试
    all_records = storage.get_all()
    print(f"\n所有记录: {len(all_records)} 条")

    # 统计测试
    stats = storage.get_statistics()
    print(f"\n统计信息: {stats}")
