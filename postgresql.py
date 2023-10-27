import psycopg2
from config import config
import tkinter as tk
from tkinter import ttk, Toplevel


class ConnectionToDatabase:
    def __init__(self):
        super().__init__()

        try:
            params = config()
            print("Connecting to the PostgreSQL database...")
            self.connection = psycopg2.connect(**params)

            cursor = self.connection.cursor()
            print("PostgreSQL Database Version:")
            cursor.execute("SELECT version()")
            db_version = cursor.fetchone()
            print(db_version)
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def connectToDataBase(self):
        try:
            params = config()
            print("Connecting to the PostgreSQL database...")
            self.connection = psycopg2.connect(**params)

            cursor = self.connection.cursor()
            print("PostgreSQL Database Version:")
            cursor.execute("SELECT version()")
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
            cursor.execute("SELECT * FROM kullanicilar")
            result = cursor.fetchall()
            for row in result:
                print(row)
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Veritabanı Okunurken Hata Oluştu: ", error)

    def readTeacher(self):
        try:
            global infoScreenStudent
            infoScreenStudent = Toplevel()
            infoScreenStudent.title("Öğretmen Bilgileri")
            infoScreenStudent.geometry("500x200")

            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM hocalar")

            tree = ttk.Treeview(infoScreenStudent)
            tree["show"] = "headings"

            style = ttk.Style(infoScreenStudent)
            style.theme_use("clam")

            tree["columns"] = ("sicilNo", "ad", "soyad", "kontenjan", "ilgialani")

            tree.column("sicilNo", width=100, minwidth=100, anchor=tk.CENTER)
            tree.column("ad", width=100, minwidth=100, anchor=tk.CENTER)
            tree.column("soyad", width=100, minwidth=100, anchor=tk.CENTER)
            tree.column("kontenjan", width=100, minwidth=100, anchor=tk.CENTER)
            tree.column("ilgialani", width=100, minwidth=100, anchor=tk.CENTER)

            tree.heading("sicilNo", text="Okul Numarası", anchor=tk.CENTER)
            tree.heading("ad", text="Öğrenci Adı", anchor=tk.CENTER)
            tree.heading("soyad", text="Öğrenci Soyadı", anchor=tk.CENTER)
            tree.heading("kontenjan", text="Öğrenci Kontenjanı", anchor=tk.CENTER)
            tree.heading("ilgialani", text="İlgi Alanları", anchor=tk.CENTER)

            i = 0
            for row in cursor:
                tree.insert(
                    "", i, text="", values=(row[0], row[1], row[2], row[3], row[4])
                )
                i += 1

            tree.pack()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Hocalar Tablosu Okunurken Hata Oluştu: ", error)

    def readStudent(self):
        try:
            global infoScreenStudent
            infoScreenStudent = Toplevel()
            infoScreenStudent.title("Öğrenci Bilgileri")
            infoScreenStudent.geometry("500x200")

            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM ogrenciler")

            tree = ttk.Treeview(infoScreenStudent)
            tree["show"] = "headings"

            style = ttk.Style(infoScreenStudent)
            style.theme_use("clam")

            tree["columns"] = ("sicilNo", "ad", "soyad", "gpa", "aldigiderssayisi")

            tree.column("sicilNo", width=100, minwidth=100, anchor=tk.CENTER)
            tree.column("ad", width=100, minwidth=100, anchor=tk.CENTER)
            tree.column("soyad", width=100, minwidth=100, anchor=tk.CENTER)
            tree.column("gpa", width=100, minwidth=100, anchor=tk.CENTER)
            tree.column("aldigiderssayisi", width=100, minwidth=100, anchor=tk.CENTER)

            tree.heading("sicilNo", text="Okul Numarası", anchor=tk.CENTER)
            tree.heading("ad", text="Öğrenci Adı", anchor=tk.CENTER)
            tree.heading("soyad", text="Öğrenci Soyadı", anchor=tk.CENTER)
            tree.heading("gpa", text="Öğrenci Not Ortalaması", anchor=tk.CENTER)
            tree.heading(
                "aldigiderssayisi", text="Alınan Ders Sayısı", anchor=tk.CENTER
            )

            i = 0
            for row in cursor:
                tree.insert(
                    "", i, text="", values=(row[0], row[1], row[2], row[3], row[4])
                )
                i += 1

            tree.pack()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Öğrenci Bilgileri Okunurken Hata Oluştu: ", error)

    def insert(self, kullaniciAd, kullaniciSoyad, kullaniciSifre, kullaniciTur):
        try:
            cursor = self.connection.cursor()
            insert_query = "INSERT INTO kullanicilar (Ad, Soyad, Sifre, Tur) VALUES (%s, %s, %s, %s)"
            cursor.execute(
                insert_query,
                (kullaniciAd, kullaniciSoyad, kullaniciSifre, kullaniciTur),
            )
            self.connection.commit()
            cursor.close()
            print("Kullanıcı Başarıyla Eklendi.")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Veritabanına Ekleme Sırasında Hata Oluştu: ", error)

    def insertTeacher(
        self, kullaniciAd, kullaniciSoyad, kullaniciSifre, hocaKota, hocaIlgiAlani
    ):
        try:
            # self.connection.connectToDataBase()
            cursor = self.connection.cursor()

            # Insert data to kullanicilar
            insert_query = "INSERT INTO kullanicilar (Ad, Soyad, Sifre, Tur) VALUES (%s, %s, %s, %s) RETURNING SicilNo;"
            cursor.execute(
                insert_query, (kullaniciAd, kullaniciSoyad, kullaniciSifre, "ogretmen")
            )
            ogretmenSicilNo = cursor.fetchone()[0]
            cursor.close()

            # Insert data to hocalar
            cursor = self.connection.cursor()
            insert_teacher_query = "INSERT INTO hocalar (SicilNo, Ad, Soyad, Kontenjan, ilgialani) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(
                insert_teacher_query,
                (ogretmenSicilNo, kullaniciAd, kullaniciSoyad, hocaKota, hocaIlgiAlani),
            )
            self.connection.commit()
            cursor.close()
            # self.connection.disconnectToDataBase()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Veritabanına Öğretmen Ekleme Sırasında Hata Oluştu: ", error)

    def insertStudents(
        self,
        kullaniciAd,
        kullaniciSoyad,
        kullaniciSifre,
        ogrenciNotOrtalama,
        ogrenciDersSayisi,
    ):
        try:
            cursor = self.connection.cursor()
            insert_query = "INSERT INTO kullanicilar (Ad, Soyad, Sifre, Tur) VALUES (%s, %s, %s, %s) RETURNING SicilNo;"
            cursor.execute(
                insert_query, (kullaniciAd, kullaniciSoyad, kullaniciSifre, "ogrenci")
            )
            ogrenciSicilNo = cursor.fetchone()[0]
            cursor.close()
            cursor = self.connection.cursor()
            insert_student_query = "INSERT INTO ogrenciler (SicilNo, Ad, Soyad, gpa, aldigiderssayisi) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(
                insert_student_query,
                (
                    ogrenciSicilNo,
                    kullaniciAd,
                    kullaniciSoyad,
                    ogrenciNotOrtalama,
                    ogrenciDersSayisi,
                ),
            )
            self.connection.commit()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Veritabanına Öğrenci Ekleme Sırasında Hata Oluştu: ", error)

    def delete(self, sicilNo):
        try:
            cursor = self.connection.cursor()
            delete_query = "DELETE FROM kullanicilar WHERE sicilNo = %s"
            cursor.execute(delete_query, (sicilNo,))
            self.connection.commit()
            cursor.close()
            print(f"Kullanıcı {sicilNo} başarıyla silindi!")
        except (Exception, psycopg2.DatabaseError) as error:
            print(
                f"Kullanıcı {sicilNo} veritabanından silinirken bir hata oluştu!", error
            )

    def deleteTeacher(self, sicilNo):
        try:
            cursor = self.connection.cursor()
            delete_query = "DELETE FROM hocalar WHERE sicilNo = %s"
            cursor.execute(delete_query, (sicilNo,))
            self.connection.commit()
            delete_query2 = "DELETE FROM kullanicilar WHERE sicilNo = %s"
            cursor.execute(delete_query2, (sicilNo,))
            self.connection.commit()
            cursor.close()
            print(
                f"Kullanıcı {sicilNo} kullanıcılar ve hocalar tablosundan başarıyla silindi!"
            )
        except (Exception, psycopg2.DatabaseError) as error:
            print(
                f"Kullanıcı {sicilNo} kullanıcılar ve hocalar tablosundan silinirken bir hata oluştu!",
                error,
            )

    def deleteStudent(self, sicilNo):
        try:
            cursor = self.connection.cursor()
            delete_query = "DELETE FROM ogrenciler WHERE sicilNo = %s"
            cursor.execute(delete_query, (sicilNo,))
            self.connection.commit()
            delete_query2 = "DELETE FROM kullanicilar WHERE sicilNo = %s"
            cursor.execute(delete_query2, (sicilNo,))
            self.connection.commit()
            cursor.close()
            print(
                f"Kullanıcı {sicilNo} kullanıcılar ve ogrenciler tablosundan başarıyla silindi!"
            )
        except (Exception, psycopg2.DatabaseError) as error:
            print(
                f"Kullanıcı {sicilNo} kullanıcılar ve ogrenciler tablosundan silinirken bir hata oluştu!",
                error,
            )

    def login(self, sicilNo, kullaniciSifre):
        try:
            cursor = self.connection.cursor()
            query = "SELECT sicilNo FROM kullanicilar WHERE sicilNo = %s AND sifre = %s"
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

    def whoIsLogin(self, sicilNo):
        try:
            cursor = self.connection.cursor()
            query = "SELECT tur FROM kullanicilar WHERE sicilNo = %s"
            cursor.execute(query, (sicilNo,))
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
    # connect()
    connect = ConnectionToDatabase()
    connect.read()
    connect.insertTeacher("Furkan", "Göz", "furkan.goz", 3, "Yapay Zeka")
    connect.insertStudents("furkan", "karlıdağ", "furkan123", 3.31, 2)
    connect.read()
    connect.disconnectToDataBase()
