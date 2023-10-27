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

    def updateStudent(
        self, sicilNo, yeniAd, yeniSoyad, yeniNotOrtalama, yeniAldigiDersSayi
    ):
        if yeniAd != "":
            try:
                cursor = self.connection.cursor()
                update_query1 = (
                    f"UPDATE ogrenciler SET ad = '{yeniAd}' WHERE sicilNo = '{sicilNo}'"
                )
                cursor.execute(update_query1)
                self.connection.commit()
                cursor.close()

                cursor = self.connection.cursor()
                update_query2 = f"UPDATE kullanicilar SET ad = '{yeniAd}' WHERE sicilNo = '{sicilNo}'"
                cursor.execute(update_query2)
                self.connection.commit()
                cursor.close()

                print(f"Kullanıcının Yeni Adı: {yeniAd}")
            except (Exception, psycopg2.DatabaseError) as error:
                print(f"Kullanıcının Yeni Adı Değiştirilemedi! ", error)
        else:
            print("Ad Bloğuna Değer Girilmedi!")

        if yeniSoyad != "":
            try:
                cursor = self.connection.cursor()
                update_query1 = f"UPDATE ogrenciler SET soyad = '{yeniSoyad}' WHERE sicilNo = '{sicilNo}'"
                cursor.execute(update_query1)
                self.connection.commit()
                cursor.close()

                cursor = self.connection.cursor()
                update_query2 = f"UPDATE kullanicilar SET soyad = '{yeniSoyad}' WHERE sicilNo = '{sicilNo}'"
                cursor.execute(update_query2)
                self.connection.commit()
                cursor.close()

                print(f"Kullanıcının Yeni Soyadı: {yeniSoyad}")
            except (Exception, psycopg2.DatabaseError) as error:
                print(f"Kullanıcının Yeni Soyadı Değiştirilemedi! ", error)
        else:
            print("Soyad Bloğuna Değer Girilmedi!")
        if yeniNotOrtalama != "":
            try:
                cursor = self.connection.cursor()
                update_query1 = f"UPDATE ogrenciler SET gpa = '{yeniNotOrtalama}' WHERE sicilNo = '{sicilNo}'"
                cursor.execute(update_query1)
                self.connection.commit()
                cursor.close()

                print(f"Kullanıcının Yeni Not Ortalaması: {yeniNotOrtalama}")
            except (Exception, psycopg2.DatabaseError) as error:
                print(f"Kullanıcının Yeni Not Ortalaması Değiştirilemedi! ", error)
        else:
            print("Not Ortalaması Bloğuna Değer Girilmedi!")
        if yeniAldigiDersSayi != "":
            try:
                cursor = self.connection.cursor()
                update_query1 = f"UPDATE ogrenciler SET aldigiderssayisi = '{yeniAldigiDersSayi}' WHERE sicilNo = '{sicilNo}'"
                cursor.execute(update_query1)
                self.connection.commit()
                cursor.close()

                print(f"Kullanıcının Yeni Aldığı Ders Sayısı: {yeniAldigiDersSayi}")
            except (Exception, psycopg2.DatabaseError) as error:
                print(f"Kullanıcının Yeni Aldığı Ders Sayısı Değiştirilemedi! ", error)
        else:
            print("Aldığı Ders Sayısı Bloğuna Değer Girilmedi!")

    def updateTeacher(self, sicilNo, yeniAd, yeniSoyad, yeniKontenjan, yeniIlgiAlani):
        if yeniAd != "":
            try:
                cursor = self.connection.cursor()
                update_query1 = (
                    f"UPDATE hocalar SET ad = '{yeniAd}' WHERE sicilNo = '{sicilNo}'"
                )
                cursor.execute(update_query1)
                self.connection.commit()
                cursor.close()

                cursor = self.connection.cursor()
                update_query2 = f"UPDATE kullanicilar SET ad = '{yeniAd}' WHERE sicilNo = '{sicilNo}'"
                cursor.execute(update_query2)
                self.connection.commit()
                cursor.close()

                print(f"Öğretmenin Yeni Adı: {yeniAd}")
            except (Exception, psycopg2.DatabaseError) as error:
                print(f"Öğretmenin Yeni Adı Değiştirilemedi! ", error)
        else:
            print("Ad Bloğuna Değer Girilmedi!")

        if yeniSoyad != "":
            try:
                cursor = self.connection.cursor()
                update_query1 = f"UPDATE hocalar SET soyad = '{yeniSoyad}' WHERE sicilNo = '{sicilNo}'"
                cursor.execute(update_query1)
                self.connection.commit()
                cursor.close()

                cursor = self.connection.cursor()
                update_query2 = f"UPDATE kullanicilar SET soyad = '{yeniSoyad}' WHERE sicilNo = '{sicilNo}'"
                cursor.execute(update_query2)
                self.connection.commit()
                cursor.close()

                print(f"Öğretmenin Yeni Soyadı: {yeniSoyad}")
            except (Exception, psycopg2.DatabaseError) as error:
                print(f"Öğretmenin Yeni Soyadı Değiştirilemedi! ", error)
        else:
            print("Soyad Bloğuna Değer Girilmedi!")

        if yeniKontenjan != "":
            try:
                cursor = self.connection.cursor()
                update_query1 = f"UPDATE hocalar SET kontenjan = '{yeniKontenjan}' WHERE sicilNo = '{sicilNo}'"
                cursor.execute(update_query1)
                self.connection.commit()
                cursor.close()

                print(f"Öğretmenin Yeni Kontenjanı: {yeniKontenjan}")
            except (Exception, psycopg2.DatabaseError) as error:
                print(f"Öğretmenin Yeni Kontenjan Sayısı Değiştirilemedi! ", error)
        else:
            print("Kontenjan Bloğuna Değer Girilmedi!")

        if yeniIlgiAlani != "":
            try:
                cursor = self.connection.cursor()
                update_query1 = f"UPDATE hocalar SET ilgialani = '{yeniIlgiAlani}' WHERE sicilNo = '{sicilNo}'"
                cursor.execute(update_query1)
                self.connection.commit()
                cursor.close()

                print(f"Öğretmenin Yeni İlgi Alanı: {yeniIlgiAlani}")
            except (Exception, psycopg2.DatabaseError) as error:
                print(f"Öğretmenin Yeni İlgi Alanı Değiştirilemedi!", error)
        else:
            print("İlgi Alanı Bloğuna Değer Girilmedi!")

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

    def whoIsLoginName(self, sicilNo):
        try:
            cursor = self.connection.cursor()
            query = "SELECT ad, soyad FROM kullanicilar WHERE sicilNo = %s"
            cursor.execute(query, (sicilNo,))
            result = cursor.fetchone()

            name = result[0] + " " + result[1]
            if result:
                print("Giriş Sağlayan Kullanıcı: ", name)
                return name
            else:
                print(f"Giriş sağlayan kullanıcı: {None}")
                return None
        except (Exception, psycopg2.DatabaseError) as error:
            print("Kullanıcı İsim Hatası: ", error)
            return None


if __name__ == "__main__":
    # connect()
    connect = ConnectionToDatabase()
    connect.read()
    connect.whoIsLoginName(12)
    connect.disconnectToDataBase()
