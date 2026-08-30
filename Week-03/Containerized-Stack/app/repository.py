from app.database import get_connection


class PostgresTaskRepository:

    def get_all_tasks(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id, title, done FROM tasks ORDER BY id"
        )

        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        return [
            {
                "id": row[0],
                "title": row[1],
                "done": row[2]
            }
            for row in rows
        ]

    def get_task(self, task_id: int):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id, title, done FROM tasks WHERE id = %s",
            (task_id,)
        )

        row = cursor.fetchone()

        cursor.close()
        connection.close()

        if row is None:
            return None

        return {
            "id": row[0],
            "title": row[1],
            "done": row[2]
        }

    def create_task(self, title: str):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO tasks (title, done)
            VALUES (%s, %s)
            RETURNING id, title, done
            """,
            (title, False)
        )

        row = cursor.fetchone()

        connection.commit()
        cursor.close()
        connection.close()

        return {
            "id": row[0],
            "title": row[1],
            "done": row[2]
        }

    def update_task(self, task_id: int, title=None, done=None):
        existing_task = self.get_task(task_id)

        if existing_task is None:
            return None

        new_title = title if title is not None else existing_task["title"]
        new_done = done if done is not None else existing_task["done"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE tasks
            SET title = %s, done = %s
            WHERE id = %s
            RETURNING id, title, done
            """,
            (new_title, new_done, task_id)
        )

        row = cursor.fetchone()

        connection.commit()
        cursor.close()
        connection.close()

        return {
            "id": row[0],
            "title": row[1],
            "done": row[2]
        }

    def delete_task(self, task_id: int):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM tasks
            WHERE id = %s
            RETURNING id
            """,
            (task_id,)
        )

        row = cursor.fetchone()

        connection.commit()
        cursor.close()
        connection.close()

        return row is not None