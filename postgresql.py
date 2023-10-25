import psycopg2
from config import config

class ConnectionToDatabase:

    def __init__(self):
        super().__init__()

        try:
            params = config()
            print('Connecting to the PostgreSQL database...')
            self.connection = psycopg2.connect(**params)

            cursor = self.connection.cursor()
            print('PostgreSQL Database Version:')
            cursor.execute('SELECT version()')
            db_version = cursor.fetchone()
            print(db_version)
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def connectToDataBase(self):
        try:
            params = config()
            print('Connecting to the PostgreSQL database...')
            self.connection = psycopg2.connect(**params)

            cursor = self.connection.cursor()
            print('PostgreSQL Database Version:')
            cursor.execute('SELECT version()')
            db_version = cursor.fetchone()
            print(db_version)
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
    def disconnectToDataBase(self):
        try:
            self.connection.close()
            print("Disconnecting Successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Disconnecting Unsuccessful", error)

    def read(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM kullanicilar')
            result = cursor.fetchall()
            for row in result:
                print(row)
            cursor.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print('Veritabanı Okunurken Hata Oluştu: ', error)

    def insert(self, kullaniciAd, kullaniciSoyad, kullaniciSifre, kullaniciTur):
        try:
            cursor = self.connection.cursor()
            insert_query = 'INSERT INTO kullanicilar (kullaniciAd, kullaniciSoyad, kullaniciSifre, kullaniciTur) VALUES (%s, %s, %s, %s)'
            cursor.execute(insert_query, (kullaniciAd, kullaniciSoyad, kullaniciSifre, kullaniciTur))
            self.connection.commit()
            cursor.close()
            print("Kullanıcı Başarıyla Eklendi.")
        except(Exception, psycopg2.DatabaseError) as error:
            print('Veritabanına Ekleme Sırasında Hata Oluştu: ', error)

    def delete(self, sicilNo):
        try:
            cursor = self.connection.cursor()
            delete_query = 'DELETE FROM kullanicilar WHERE sicilNo = %s'
            cursor.execute(delete_query, (sicilNo,))
            self.connection.commit()
            cursor.close()
            print(f"Kullanıcı {sicilNo} başarıyla silindi!")
        except(Exception, psycopg2.DatabaseError) as error:
            print(f"Kullanıcı {sicilNo} veritabanından silinirken bir hata oluştu!", error)
    
    def login(self, sicilNo, kullaniciSifre):
        try:
            cursor = self.connection.cursor()
            query = "SELECT sicilNo FROM kullanicilar WHERE sicilNo = %s AND kullaniciSifre = %s"
            cursor.execute(query, (sicilNo, kullaniciSifre))
            result = cursor.fetchone()
            cursor.close()

            if result:
                print("Login Succsesfully")
                return True
            else:
                print("Login Unsuccsesfully")
                return False
            
        except (Exception, psycopg2.DatabaseError) as error:
            print("Veritabanı Hatası: ", error)

    def whoIsLogin(self, sicilNo, kullaniciSifre):
        try:
            cursor = self.connection.cursor()
            query = "SELECT kullaniciTur FROM kullanicilar WHERE sicilNo = %s AND kullaniciSifre = %s"
            cursor.execute(query, (sicilNo, kullaniciSifre))
            result = cursor.fetchone()

            if result:
                print("Giriş sağlayan kullanıcı Türü: ", result[0])
                return result[0]
            else:
                print(f"Giriş sağlayan kullanıcı Türü: {None}")
                return None
        except (Exception, psycopg2.DatabaseError) as error:
            print("Veritabanı Hatası: ", error)
            return None

if __name__ == "__main__":
    #connect()
    connect = ConnectionToDatabase()
    connect.delete(2)
    connect.read()
    connect.disconnectToDataBase()