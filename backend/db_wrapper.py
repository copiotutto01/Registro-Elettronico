import pymysql

class DatabaseWrapper:
    def __init__(self, host='mysql-3f12020f-galvani5d.j.aivencloud.com', user='avnadmin', password='AVNS_idAGBvmY7bsHyDkUXBM', database='defaultdb', port=13861):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Database connected successfully")
        except pymysql.Error as e:
            print(f"Database connection error: {e}")
            raise

    def insert_vote(self, student_name, subject, vote):
        try:
            if not self.connection or not self.connection.open:
                self.connect()
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO votes (student_name, subject, vote) VALUES (%s, %s, %s)"
                cursor.execute(sql, (student_name, subject, vote))
            self.connection.commit()
            print(f"Vote inserted for {student_name} in {subject}: {vote}")
        except pymysql.Error as e:
            print(f"Error inserting vote: {e}")
            raise

    def get_all_votes(self):
        try:
            if not self.connection or not self.connection.open:
                self.connect()
            with self.connection.cursor() as cursor:
                sql = "SELECT id, student_name, subject, vote FROM votes ORDER BY id DESC"
                cursor.execute(sql)
                result = cursor.fetchall()
            return result if result else []
        except pymysql.Error as e:
            print(f"Error fetching all votes: {e}")
            return []

    def get_votes_by_student(self, student_name):
        try:
            if not self.connection or not self.connection.open:
                self.connect()
            with self.connection.cursor() as cursor:
                sql = "SELECT id, subject, vote FROM votes WHERE student_name = %s ORDER BY id DESC"
                cursor.execute(sql, (student_name,))
                result = cursor.fetchall()
            return result if result else []
        except pymysql.Error as e:
            print(f"Error fetching votes for {student_name}: {e}")
            return []

    def get_subjects(self):
        try:
            if not self.connection or not self.connection.open:
                self.connect()
            with self.connection.cursor() as cursor:
                sql = "SELECT DISTINCT subject FROM votes ORDER BY subject"
                cursor.execute(sql)
                result = cursor.fetchall()
            return [row['subject'] for row in result] if result else []
        except pymysql.Error as e:
            print(f"Error fetching subjects: {e}")
            return []

    def get_students(self):
        try:
            if not self.connection or not self.connection.open:
                self.connect()
            with self.connection.cursor() as cursor:
                sql = "SELECT DISTINCT student_name FROM votes ORDER BY student_name"
                cursor.execute(sql)
                result = cursor.fetchall()
            return [row['student_name'] for row in result] if result else []
        except pymysql.Error as e:
            print(f"Error fetching students: {e}")
            return []

    def close(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed")
