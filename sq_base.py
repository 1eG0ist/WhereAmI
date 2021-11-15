import sqlite3

class SQLighter:

    def __init__(self, database_file):
        """~~~Подключаемся к БД и сохраняем курсор соединения~~~"""
        
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status = True):
        """ Получаем всех активные пользователи бота"""
        with self.connection:
            return self.curcor.execute("SELECT * FROM 'user_build' WHERE 'status' = ?", (status,)).fetchall()
    
