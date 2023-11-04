import psycopg2
from config import config
import tkinter as tk
from tkinter import ttk, Toplevel, Label, Entry, Button
from PyPDF2 import PdfReader
import re
import random


class ConnectionToDatabase:
    def __init__(self):
        super().__init__()
        self.treeTeacher = None

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
        self, sicilNo, yeniAd, yeniSoyad, yeniSifre, yeniNotOrtalama, yeniAldigiDersSayi
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

        if yeniSifre != "":
            try:
                cursor = self.connection.cursor()
                update_query2 = f"UPDATE kullanicilar SET sifre= '{yeniSifre}' WHERE sicilNo = '{sicilNo}'"
                cursor.execute(update_query2)
                self.connection.commit()
                cursor.close()

                print(f"Öğrencinin Yeni Şifresi: {yeniSifre}")
            except (Exception, psycopg2.DatabaseError) as error:
                print(
                    "Öğrencinin Şifresi Değiştirilirken Hata ile Karşılaşıldı: ", error
                )
        else:
            print("Şifre Bloğuna Değer Girilmedi!")

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

    def updateTeacher(
        self, sicilNo, yeniAd, yeniSoyad, yeniSifre, yeniKontenjan, yeniIlgiAlani
    ):
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

        if yeniSifre != "":
            try:
                cursor = self.connection.cursor()
                update_query2 = f"UPDATE kullanicilar SET sifre= '{yeniSifre}' WHERE sicilNo = '{sicilNo}'"
                cursor.execute(update_query2)
                self.connection.commit()
                cursor.close()

                print(f"Öğretmenin Yeni Şifresi: {yeniSifre}")
            except (Exception, psycopg2.DatabaseError) as error:
                print(
                    "Öğretmenin Şifresi Değiştirilirken Hata ile Karşılaşıldı: ", error
                )
        else:
            print("Şifre Bloğuna Değer Girilmedi!")

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

    def insertTranscript(self, username, file):
        # file = "/Users/veliashvili/Desktop/yazlab1.3/metehan-belli-transkript.pdf"
        reader = PdfReader(file)
        total_pages = len(reader.pages)

        codes = []
        courses = []
        for page_num in range(total_pages - 1):
            page = reader.pages[page_num]
            text = page.extract_text()
            for line in text.split("\n"):
                matches = re.findall(r"[A-Z]{3}\d{3}", line)
                if matches:
                    for match in matches:
                        codes.append(match)
                        courses.append(line)

        codes.pop(17)
        courses.pop(17)

        for i in range(len(courses)):
            courses[i] = courses[i][7:]

        grades = []
        for page_num in range(total_pages - 1):
            page = reader.pages[page_num]
            text = page.extract_text()
            for line in text.split("\n"):
                matches = re.findall(r"AA|BA|BB|CB|CC|DC|DD|FD|FF", line)
                if matches:
                    for match in matches:
                        grades.append(match)

        try:
            for i in range(len(courses)):
                cursor = self.connection.cursor()
                insert_query = "INSERT INTO ogrenciDersler (sicilNo, dersKodu, dersAdi, harfNotu) VALUES (%s, %s, %s, %s)"
                cursor.execute(
                    insert_query, (username, codes[i], courses[i], grades[i])
                )
                self.connection.commit()
                cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Ders Tablosuna Ekleme Yapılırken Hata ile Karşılaşıldı: ", error)

    def deleteCourses(self, username, file):
        reader = PdfReader(file)
        total_pages = len(reader.pages)

        codes = []
        for page_num in range(total_pages - 1):
            page = reader.pages[page_num]
            text = page.extract_text()
            for line in text.split("\n"):
                matches = re.findall(r"[A-Z]{3}\d{3}", line)
                if matches:
                    for match in matches:
                        codes.append(match)

        codes.pop(17)

        try:
            for i in range(len(codes)):
                cursor = self.connection.cursor()
                delete_query = (
                    "DELETE FROM ogrenciDersler WHERE sicilNo = %s AND dersKodu = %s"
                )
                cursor.execute(delete_query, (username, codes[i]))
                self.connection.commit()
                cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Dersler Silinirken Bir Hata Oluştu: ", error)

    def readTranscriptsData(self):
        try:
            global infoScreenTranscript
            infoScreenTranscript = Toplevel()
            infoScreenTranscript.title("Verilen Ders Bilgileri")
            infoScreenTranscript.geometry("503x228")

            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM ogrenciDersler")

            tree = ttk.Treeview(infoScreenTranscript)
            tree["show"] = "headings"

            style = ttk.Style(infoScreenTranscript)
            style.theme_use("clam")

            tree["columns"] = ("sicilno", "derskodu", "dersadi", "harfnotu")
            tree.column("sicilno", width=100, minwidth=100, anchor=tk.CENTER)
            tree.column("derskodu", width=100, minwidth=100, anchor=tk.CENTER)
            tree.column("dersadi", width=200, minwidth=100, anchor=tk.CENTER)
            tree.column("harfnotu", width=100, minwidth=100, anchor=tk.CENTER)

            tree.heading("sicilno", text="Sicil No", anchor=tk.CENTER)
            tree.heading("derskodu", text="Ders Kodu", anchor=tk.CENTER)
            tree.heading("dersadi", text="Ders Adı", anchor=tk.CENTER)
            tree.heading("harfnotu", text="Harf Notu", anchor=tk.CENTER)

            i = 0
            for row in cursor:
                tree.insert("", i, text="", values=(row[0], row[1], row[2], row[3]))
                i += 1

            tree.pack()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Transkript Okunurken Hata Oluştu: ", error)

    def sendMessage(self, gonderenSicilNo, aliciSicilNo, tur, mesaj_icerigi):
        try:
            cursor = self.connection.cursor()
            send_query = "INSERT INTO mesajlar (timestamp, gonderenSicilNo, aliciSicilNo, tur, mesaj_icerigi) VALUES (NOW(), %s, %s, %s, %s)"
            cursor.execute(
                send_query, (gonderenSicilNo, aliciSicilNo, tur, mesaj_icerigi)
            )
            self.connection.commit()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Mesaj Gönderilirken Bir Hata Oluştu: ", error)

    def readMessage(self, aliciNo):
        try:
            global infoScreenMessages
            infoScreenMessages = Toplevel()
            infoScreenMessages.title("Gelen Kutusu")
            infoScreenMessages.geometry("1070x200")

            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM mesajlar WHERE aliciSicilNo = %s", (aliciNo,))

            tree = ttk.Treeview(infoScreenMessages)
            tree["show"] = "headings"

            style = ttk.Style(infoScreenMessages)
            style.theme_use("clam")

            tree["columns"] = (
                "timestamp",
                "mesajno",
                "gonderenno",
                "alicino",
                "tur",
                "mesaj_icerigi",
            )
            tree.column("timestamp", width=100, minwidth=100, anchor=tk.CENTER)
            tree.column("mesajno", width=100, minwidth=100, anchor=tk.CENTER)
            tree.column("gonderenno", width=200, minwidth=100, anchor=tk.CENTER)
            tree.column("alicino", width=100, minwidth=100, anchor=tk.CENTER)
            tree.column("tur", width=100, minwidth=100, anchor=tk.CENTER)
            tree.column("mesaj_icerigi", width=500, minwidth=100, anchor=tk.CENTER)

            tree.heading("timestamp", text="Gönderilme Zamanı", anchor=tk.CENTER)
            tree.heading("mesajno", text="Mesaj Numarası", anchor=tk.CENTER)
            tree.heading("gonderenno", text="Gönderici Numarası", anchor=tk.CENTER)
            tree.heading("alicino", text="Alıcı Numarası", anchor=tk.CENTER)
            tree.heading("tur", text="Gönderenin Türü", anchor=tk.CENTER)
            tree.heading("mesaj_icerigi", text="Mesaj", anchor=tk.CENTER)

            i = 0
            for row in cursor:
                tree.insert(
                    "",
                    i,
                    text="",
                    values=(row[0], row[1], row[2], row[3], row[4], row[5]),
                )
                i += 1

            tree.pack()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Gelen Kutusu Okunurken Hata Oluştu: ", error)

    def readInterest(self, sicilNo):
        try:
            cursor = self.connection.cursor()
            read_query = "SELECT ilgialani FROM hocalar WHERE sicilNo = %s"
            cursor.execute(read_query, (sicilNo,))
            data = cursor.fetchone()

            if data:
                ilgialani = data[0]
                print(f"Sicil No: {sicilNo} için İlgi Alanı: {ilgialani}")
                return ilgialani
            else:
                print(f"Sicil No {sicil_no} için kayıt bulunamadı.")
                return None

            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print("İlgi Alanı Okunurken Bir hata ile Karşılaşıldı: ", error)

    def updateInterests(self, sicilNo, ilgiAlani):
        try:
            cursor = self.connection.cursor()
            update_query = "UPDATE hocalar SET ilgialani = %s WHERE sicilNo = %s"
            cursor.execute(update_query, (ilgiAlani, sicilNo))
            self.connection.commit()
            cursor.close()
            print(f"Sicil No {sicilNo} için ilgi alanları güncellendi.")
        except (Exception, psycopg2.DatabaseError) as error:
            print("İlgi Alanlarınız Güncellenirken Hata ile Karşılaşıldı: ", error)

    def readTeacherScreen(self):
        try:
            global teacherDataScreen
            teacherDataScreen = Toplevel()
            teacherDataScreen.title("Öğretmen Bilgileri")
            teacherDataScreen.geometry("604x300")

            label = Label(teacherDataScreen, text="Filtreleme: ")
            label.place(x=100, y=250, anchor="nw")

            entry = Entry(teacherDataScreen)
            entry.place(x=200, y=250, anchor="nw")

            button = Button(
                teacherDataScreen,
                text="FİLTRELE",
                command=lambda: self.filterTeacher(entry.get()),
            )
            button.place(x=400, y=250, anchor="nw")
            self.showAllTeachers()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Hocalar Tablosu Okunurken Hata Oluştu: ", error)

    def showAllTeachers(self):
        self.connectToDataBase()
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM hocalar")

        self.treeTeacher = ttk.Treeview(teacherDataScreen)
        self.treeTeacher["show"] = "headings"

        style = ttk.Style(teacherDataScreen)
        style.theme_use("clam")

        self.treeTeacher["columns"] = (
            "sicilno",
            "ad",
            "soyad",
            "kontenjan",
            "ilgialani",
        )
        self.treeTeacher.column("sicilno", width=100, minwidth=100, anchor=tk.CENTER)
        self.treeTeacher.column("ad", width=100, minwidth=100, anchor=tk.CENTER)
        self.treeTeacher.column("soyad", width=100, minwidth=100, anchor=tk.CENTER)
        self.treeTeacher.column("kontenjan", width=100, minwidth=100, anchor=tk.CENTER)
        self.treeTeacher.column("ilgialani", width=200, minwidth=100, anchor=tk.CENTER)

        self.treeTeacher.heading("sicilno", text="Hoca Okul No", anchor=tk.CENTER)
        self.treeTeacher.heading("ad", text="Ad", anchor=tk.CENTER)
        self.treeTeacher.heading("soyad", text="Soyad", anchor=tk.CENTER)
        self.treeTeacher.heading("kontenjan", text="Kontenjan", anchor=tk.CENTER)
        self.treeTeacher.heading("ilgialani", text="İlgi Alanı", anchor=tk.CENTER)

        i = 0
        for row in cursor:
            self.treeTeacher.insert(
                "",
                i,
                text="",
                values=(row[0], row[1], row[2], row[3], row[4]),
            )
            i += 1

        self.treeTeacher.pack()
        self.disconnectToDataBase()

    def filterTeacher(self, ilgialani):
        if ilgialani == "":
            # Başlangıç halini göstermem lazım!
            self.showAllTeachers()
        else:
            self.connectToDataBase()
            for item in self.treeTeacher.get_children():
                self.treeTeacher.delete(item)

            cursor = self.connection.cursor()
            filter_query = "SELECT * FROM hocalar WHERE ilgialani= %s"
            cursor.execute(filter_query, (ilgialani,))

            i = 0
            for row in cursor:
                self.treeTeacher.insert(
                    "",
                    i,
                    text="",
                    values=(row[0], row[1], row[2], row[3], row[4]),
                )
                i += 1

            self.disconnectToDataBase()

    def requests(self, gonderenNo, aliciNo, dersAdi, talepSonuc):
        self.connectToDataBase()
        try:
            cursor = self.connection.cursor()
            request_query = "INSERT INTO talepler (gonderenNo, aliciNo, dersIsmi, talepSonuc) VALUES (%s, %s, %s, %s)"
            cursor.execute(request_query, (gonderenNo, aliciNo, dersAdi, talepSonuc))
            self.connection.commit()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Öğrencinin Talebi İletilirken Bir Hata ile Karşılaşıldı: ", error)
        self.disconnectToDataBase()

    def readRequests(self, aliciNo):
        try:
            global talepScreen
            talepScreen = Toplevel()
            talepScreen.title("Talep Bilgileri")
            talepScreen.geometry("853x350")

            tree = ttk.Treeview(talepScreen)
            tree["show"] = "headings"

            style = ttk.Style(talepScreen)
            style.theme_use("clam")

            cursor = self.connection.cursor()
            sql_query = """
            SELECT ogrenciler.ad, ogrenciler.soyad, talepler.gondermezamani, talepler.talepno ,talepler.gonderenno,
            talepler.dersismi, talepler.talepsonuc 
            FROM talepler
            JOIN ogrenciler ON talepler.gonderenno = ogrenciler.sicilno
            WHERE talepler.alicino = %s;
            """

            cursor.execute(sql_query, (aliciNo,))

            tree["columns"] = (
                "ad",
                "soyad",
                "timestamp",
                "talepno",
                "gonderenno",
                "dersismi",
                "talepsonuc",
            )
            tree.column("ad", width=100, minwidth=100, anchor=tk.CENTER)
            tree.column("soyad", width=100, minwidth=100, anchor=tk.CENTER)
            tree.column("timestamp", width=150, minwidth=100, anchor=tk.CENTER)
            tree.column("talepno", width=50, minwidth=100, anchor=tk.CENTER)
            tree.column("gonderenno", width=50, minwidth=100, anchor=tk.CENTER)
            tree.column("dersismi", width=150, minwidth=100, anchor=tk.CENTER)
            tree.column("talepsonuc", width=250, minwidth=100, anchor=tk.CENTER)

            tree.heading("ad", text="Ad", anchor=tk.CENTER)
            tree.heading("soyad", text="Soyad", anchor=tk.CENTER)
            tree.heading("timestamp", text="Gönderilme Zamanı", anchor=tk.CENTER)
            tree.heading("talepno", text="Talep Numarası", anchor=tk.CENTER)
            tree.heading("gonderenno", text="Gönderici Numarası", anchor=tk.CENTER)
            tree.heading("dersismi", text="Ders Adı", anchor=tk.CENTER)
            tree.heading("talepsonuc", text="Talep Durumu", anchor=tk.CENTER)

            i = 0
            for row in cursor:
                tree.insert(
                    "",
                    i,
                    text="",
                    values=(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        row[5],
                        row[6],
                    ),
                )
                i += 1

            tree.grid(row=0, columnspan=7)

            Label(talepScreen, text="Talep Numarası: ").grid(row=1, column=0)
            requestEntry = Entry(talepScreen)
            requestEntry.grid(row=1, column=1)
            Button(
                talepScreen,
                text="ONAYLA",
                command=lambda: self.requestAccept(requestEntry.get()),
            ).grid(row=1, column=2)
            Button(
                talepScreen,
                text="REDDET",
                command=lambda: self.requestReject(requestEntry.get()),
            ).grid(row=1, column=3)

        except (Exception, psycopg2.DatabaseError) as error:
            print("Talepler Listelenirken Hata Oluştu: ", error)

    def requestAccept(self, talepno):
        self.connectToDataBase()
        try:
            cursor = self.connection.cursor()
            control_query = "SELECT kontenjan FROM hocalar WHERE sicilno = (SELECT alicino FROM talepler WHERE talepno = %s)"
            cursor.execute(control_query, (talepno,))
            resultKontenjan = cursor.fetchone()

            global infoScreenAccept
            infoScreenAccept = Toplevel()

            if resultKontenjan and resultKontenjan[0] > 0:
                cursor = self.connection.cursor()
                accept_query = "UPDATE talepler SET talepsonuc= %s WHERE talepno = %s AND talepsonuc = %s"
                cursor.execute(accept_query, ("Onaylandı", talepno, "Değerlendirmede"))
                self.connection.commit()
                cursor.close()

                reduce_kontenjan_query = "UPDATE hocalar SET kontenjan = kontenjan - 1 WHERE sicilno = (SELECT alicino FROM talepler WHERE talepno = %s)"
                cursor = self.connection.cursor()
                cursor.execute(reduce_kontenjan_query, (talepno,))
                self.connection.commit()
                cursor.close()

                cursor = self.connection.cursor()
                read_query = "SELECT talepsonuc FROM talepler WHERE talepno = %s"
                cursor.execute(read_query, (talepno,))
                result = cursor.fetchone()
                cursor.close()

                if result and result[0] == "Onaylandı":
                    infoScreenAccept.title("Talep Kabul Edildi!")
                    Label(
                        infoScreenAccept, text="Talebi Başarıyla Kabul Ettiniz!"
                    ).grid(row=0, column=0)
                    Button(
                        infoScreenAccept,
                        text="Tamam",
                        command=lambda: infoScreenAccept.withdraw(),
                    ).grid(row=1, column=0)
                    infoScreenAccept.deiconify()
                else:
                    infoScreenAccept.title("Talep Kabul Edilirken Hata Oluştu!")
                    Label(
                        infoScreenAccept,
                        text="Lütfen Geçerli Bir Talep Numarası Giriniz!",
                    ).grid(row=0, column=0)
                    Button(
                        infoScreenAccept,
                        text="Tamam",
                        command=lambda: infoScreenAccept.withdraw(),
                    ).grid(row=1, column=0)
                    infoScreenAccept.deiconify()
            else:
                infoScreenAccept.title("Kontenjan Yetersiz!")
                Label(
                    infoScreenAccept,
                    text="Kontenjanınız Dolu! Lütfen Yöneticiniz ile İletişime Geçiniz!",
                ).grid(row=0, column=0)
                Button(
                    infoScreenAccept,
                    text="Tamam",
                    command=lambda: infoScreenAccept.withdraw(),
                ).grid(row=1, column=0)
                infoScreenAccept.deiconify()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Talep Kabul Edilirken Hata ile Karşılaşıldı: ", error)
        self.disconnectToDataBase()

    def requestReject(self, talepno):
        self.connectToDataBase()
        try:
            cursor = self.connection.cursor()
            reject_query = "UPDATE talepler SET talepsonuc = %s WHERE talepno = %s AND talepsonuc = %s"
            cursor.execute(reject_query, ("Reddedildi", talepno, "Değerlendirmede"))
            self.connection.commit()
            cursor.close()

            cursor = self.connection.cursor()
            read_query = "SELECT talepsonuc FROM talepler WHERE talepno = %s"
            cursor.execute(read_query, (talepno,))
            result = cursor.fetchone()

            global infoScreenReject
            infoScreenReject = Toplevel()
            if result and result[0] == "Reddedildi":
                infoScreenReject.title("Talep Reddedildi!")
                Label(infoScreenReject, text="Talebi Başarıyla Reddettiniz!").grid(
                    row=0, column=0
                )
                Button(
                    infoScreenReject,
                    text="Tamam",
                    command=lambda: infoScreenReject.withdraw(),
                ).grid(row=1, column=0)
                infoScreenReject.deiconify()
            else:
                infoScreenReject.title("Reddedilirken Hata Oluştu!")
                Label(
                    infoScreenReject, text="Lütfen Geçerli Bir Talep Numarası Giriniz!"
                ).grid(row=0, column=0)
                Button(
                    infoScreenReject,
                    text="Tamam",
                    command=lambda: infoScreenReject.withdraw(),
                ).grid(row=1, column=0)
                infoScreenReject.deiconify()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Talep Reddedilirken Hata ile Karşılaşıldı: ", error)
        self.disconnectToDataBase()

    def lessons(self, username):
        try:
            global talepScreen
            talepScreen = Toplevel()
            talepScreen.title("Alınan Ders Bilgileri")
            talepScreen.geometry("553x225")

            tree = ttk.Treeview(talepScreen)
            tree["show"] = "headings"

            style = ttk.Style(talepScreen)
            style.theme_use("clam")

            cursor = self.connection.cursor()

            sql_query = """
            SELECT hocalar.sicilno, hocalar.ad, hocalar.soyad,
            talepler.dersismi
            FROM talepler
            JOIN hocalar ON talepler.alicino = hocalar.sicilno
            WHERE talepler.gonderenno = %s AND talepler.talepsonuc = %s;
            """

            cursor.execute(sql_query, (username, "Onaylandı"))

            tree["columns"] = (
                "sicilno",
                "ad",
                "soyad",
                "dersismi",
            )
            tree.column("sicilno", width=150, minwidth=100, anchor=tk.CENTER)
            tree.column("ad", width=100, minwidth=100, anchor=tk.CENTER)
            tree.column("soyad", width=100, minwidth=100, anchor=tk.CENTER)
            tree.column("dersismi", width=200, minwidth=100, anchor=tk.CENTER)

            tree.heading("sicilno", text="Öğretmen Okul No", anchor=tk.CENTER)
            tree.heading("ad", text="Ad", anchor=tk.CENTER)
            tree.heading("soyad", text="Soyad", anchor=tk.CENTER)
            tree.heading("dersismi", text="Ders Adı", anchor=tk.CENTER)

            i = 0
            for row in cursor:
                tree.insert(
                    "",
                    i,
                    text="",
                    values=(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                    ),
                )
                i += 1

            tree.pack()
            cursor.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Dersleriniz Okunurken Hata ile Karşılaşıldı: ", error)

    def insertLessons(self, username):
        try:
            cursor = self.connection.cursor()
            cursor2 = self.connection.cursor()

            sql_query = """
            SELECT hocalar.sicilno, hocalar.ad, hocalar.soyad,
            talepler.dersismi
            FROM talepler
            JOIN hocalar ON talepler.alicino = hocalar.sicilno
            WHERE talepler.gonderenno = %s AND talepler.talepsonuc = %s;"""

            cursor.execute(sql_query, (username, "Onaylandı"))
            i = 0
            for row in cursor:
                insert_query = """
                INSERT INTO alinandersler (sicilno, dersadi, ogretmenad, ogretmensoyad)
                VALUES (%s, %s, %s, %s)
                """
                insert_data = (row[0], row[3], row[1], row[2])

                cursor2.execute(insert_query, insert_data)
                self.connection.commit()
                i += 1

            cursor.close()
            cursor2.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Ekleme Yapılırken Hata ile Karşılaşıldı: ", error)

    def deleteLessons(self, username):
        try:
            cursor = self.connection.cursor()
            delete_query = "DELETE FROM alinandersler WHERE sicilno = %s"
            cursor.execute(delete_query, (username,))
            self.connection.commit()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Dersleriniz Silinirken Hata ile Karşılaşıldı: ", error)

    def oldRequests(self, gonderenNo):
        try:
            global eskiTalepScreen
            eskiTalepScreen = Toplevel()
            eskiTalepScreen.title("Talep Bilgileri")
            eskiTalepScreen.geometry("818x300")  # y = 225

            tree = ttk.Treeview(eskiTalepScreen)
            tree["show"] = "headings"

            style = ttk.Style(eskiTalepScreen)
            style.theme_use("clam")

            cursor = self.connection.cursor()
            sql_query = """
            SELECT hocalar.ad, hocalar.soyad, talepler.gondermezamani, talepler.talepno ,talepler.alicino,
            talepler.dersismi, talepler.talepsonuc 
            FROM talepler
            JOIN hocalar ON talepler.alicino = hocalar.sicilno
            WHERE talepler.gonderenno = %s;
            """
            cursor.execute(sql_query, (gonderenNo,))

            tree["columns"] = (
                "ad",
                "soyad",
                "timestamp",
                "talepno",
                "alicino",
                "dersismi",
                "talepsonuc",
            )
            tree.column("ad", width=100, minwidth=100, anchor=tk.CENTER)
            tree.column("soyad", width=100, minwidth=100, anchor=tk.CENTER)
            tree.column("timestamp", width=150, minwidth=100, anchor=tk.CENTER)
            tree.column("talepno", width=50, minwidth=100, anchor=tk.CENTER)
            tree.column("alicino", width=50, minwidth=100, anchor=tk.CENTER)
            tree.column("dersismi", width=150, minwidth=100, anchor=tk.CENTER)
            tree.column("talepsonuc", width=215, minwidth=100, anchor=tk.CENTER)

            tree.heading("ad", text="Ad", anchor=tk.CENTER)
            tree.heading("soyad", text="Soyad", anchor=tk.CENTER)
            tree.heading("timestamp", text="Gönderilme Zamanı", anchor=tk.CENTER)
            tree.heading("talepno", text="Talep Numarası", anchor=tk.CENTER)
            tree.heading("alicino", text="Alıcı Numarası", anchor=tk.CENTER)
            tree.heading("dersismi", text="Ders Adı", anchor=tk.CENTER)
            tree.heading("talepsonuc", text="Talep Durumu", anchor=tk.CENTER)

            i = 0
            for row in cursor:
                tree.insert(
                    "",
                    i,
                    text="",
                    values=(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        row[5],
                        row[6],
                    ),
                )
                i += 1

            tree.grid(row=0, columnspan=7)
            cursor.close()

            Label(eskiTalepScreen, text="Talep Numarası: ").grid(
                row=1, column=0, sticky="w"
            )
            entrySilinicekNo = Entry(eskiTalepScreen)
            entrySilinicekNo.grid(row=1, column=1, sticky="w")

            entrySilinecekNoButton = Button(
                eskiTalepScreen,
                text="SİL",
                command=lambda: self.deleteTalep(entrySilinicekNo.get()),
            )
            entrySilinecekNoButton.grid(row=1, column=2, sticky="w")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Öğrencinin Talepleri Listelenirken Hata Oluştu: ", error)

    def deleteTalep(self, talepNo):
        try:
            self.connectToDataBase()
            cursor = self.connection.cursor()
            delete_query = "DELETE FROM talepler WHERE talepno=%s AND talepsonuc=%s"
            cursor.execute(delete_query, (talepNo, "Değerlendirmede"))
            self.connection.commit()
            cursor.close()
            self.disconnectToDataBase()

            global infoScreenDelete
            infoScreenDelete = Toplevel()
            infoScreenDelete.title("İşlem Başarılı!")
            Label(infoScreenDelete, text="Başarıyla Talebiniz Silindi!").grid(
                row=0, column=0
            )
            Button(
                infoScreenDelete,
                text="Tamam",
                command=lambda: infoScreenDelete.withdraw(),
            ).grid(row=1, column=0)
            infoScreenDelete.deiconify()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Talebiniz Silinirken Hata Oluştu: ", error)

    def deleteRequestAll(self):
        try:
            cursor = self.connection.cursor()
            delete_query = "DELETE FROM alinandersler"
            cursor.execute(delete_query)
            self.connection.commit()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Silme İşlemi Sırasında hata ile Karşılaşıldı: ", error)

    # Öğrenci Listele
    def showFreeStudents(self):
        try:
            cursor = self.connection.cursor()
            cursor2 = self.connection.cursor()
            read_query = (
                "SELECT gonderenno, dersismi FROM talepler WHERE talepsonuc = %s"
            )
            cursor.execute(read_query, ("Onaylandı",))
            results = cursor.fetchall()

            cursor2.execute("SELECT sicilno FROM ogrenciler")
            results2 = cursor2.fetchall()
            ogrenciler = [result[0] for result in results2]

            ogrenciler_sonuc = [
                result[0] for result in results if result[0] in ogrenciler
            ]

            for ogrenci_sonuc in ogrenciler_sonuc:
                if ogrenci_sonuc in ogrenciler:
                    ogrenciler.remove(ogrenci_sonuc)
            cursor.close()
            cursor2.close()
            return ogrenciler
        except (Exception, psycopg2.DatabaseError) as error:
            print("Boştaki Öğrenciler Gösterilirken Hata ile Karşılaşıldı: ", error)

    def dersTalebiEkraniHoca(self, username):
        try:
            cursor = self.connection.cursor()
            dataAd = []
            data = []
            data = self.showFreeStudents()
            i = 0
            for i in range(len(data)):
                read_query = "SELECT ad FROM ogrenciler WHERE sicilno = %s"
                cursor.execute(read_query, (data[i],))
                result = cursor.fetchone()
                dataAd.append(result[0])
                i += 1
            cursor.close()

            cursor = self.connection.cursor()
            dataSoyad = []
            data2 = self.showFreeStudents()
            j = 0
            for j in range(len(data2)):
                read_query = "SELECT soyad FROM ogrenciler WHERE sicilno = %s"
                cursor.execute(read_query, (data[j],))
                result = cursor.fetchone()
                dataSoyad.append(result[0])
                j += 1
            cursor.close()

            cursor = self.connection.cursor()
            dataGPA = []
            k = 0
            for k in range(len(data)):
                read_query = "SELECT gpa FROM ogrenciler WHERE sicilno = %s"
                cursor.execute(read_query, (data[k],))
                result = cursor.fetchone()
                dataGPA.append(result[0])
                k += 1
            cursor.close()
            listedData = list(zip(data, dataAd, dataSoyad, dataGPA))

            global dersTalebiHocaScreen
            dersTalebiHocaScreen = Toplevel()
            dersTalebiHocaScreen.title("Lütfen Öğrencinizi Talep Ediniz!")
            dersTalebiHocaScreen.geometry("803x555")

            tree = ttk.Treeview(dersTalebiHocaScreen)
            tree["show"] = "headings"

            style = ttk.Style(dersTalebiHocaScreen)
            style.theme_use("clam")

            tree["columns"] = (
                "sicilno",
                "ad",
                "soyad",
                "gpa",
            )
            tree.column("sicilno", width=200, minwidth=100, anchor=tk.CENTER)
            tree.column("ad", width=200, minwidth=100, anchor=tk.CENTER)
            tree.column("soyad", width=200, minwidth=100, anchor=tk.CENTER)
            tree.column("gpa", width=200, minwidth=100, anchor=tk.CENTER)

            tree.heading("sicilno", text="Okul Numarası", anchor=tk.CENTER)
            tree.heading("ad", text="Ad", anchor=tk.CENTER)
            tree.heading("soyad", text="Soyad", anchor=tk.CENTER)
            tree.heading("gpa", text="Not Ortalaması", anchor=tk.CENTER)

            i = 0
            for row in listedData:
                tree.insert(
                    "",
                    i,
                    text="",
                    values=(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                    ),
                )
                i += 1
            tree.grid(row=0, columnspan=5)

            Label(dersTalebiHocaScreen, text="Öğrencinin Ders Bilgileri").grid(
                row=1, column=0
            )
            combo = ttk.Combobox(dersTalebiHocaScreen, values=data)
            combo.set("Öğrenci Numarası")
            combo.grid(row=1, column=1)
            dersBilgiButton = Button(
                dersTalebiHocaScreen,
                text="Bilgi Gör",
                command=lambda: self.dersBilgiGetir(combo.get()),
            )
            dersBilgiButton.grid(row=1, column=2)

            Label(dersTalebiHocaScreen, text="Öğrenciye Ders Talebi Yollama").grid(
                row=3, column=0
            )
            combo2 = ttk.Combobox(dersTalebiHocaScreen, values=data)
            combo2.set("Öğrenci Numarası")
            combo2.grid(row=3, column=1)

            combo3 = ttk.Combobox(
                dersTalebiHocaScreen, values=["Araştırma Projesi", "Bitirme Projesi"]
            )
            combo3.set("Dersin Adı")
            combo3.grid(row=3, column=2)
            talepButton = Button(
                dersTalebiHocaScreen,
                text="Talep Gönder",
                command=lambda: self.requests(
                    username, combo2.get(), combo3.get(), "Değerlendirmede"
                ),
            )
            talepButton.grid(row=3, column=3)

        except (Exception, psycopg2.DatabaseError) as error:
            print("Hata ile Karşılaşıldı: ", error)

    def dersBilgiGetir(self, username):
        self.connectToDataBase()
        tree2 = ttk.Treeview(dersTalebiHocaScreen)
        tree2["show"] = "headings"

        style = ttk.Style(dersTalebiHocaScreen)
        style.theme_use("clam")

        tree2["columns"] = (
            "derskodu",
            "dersadi",
            "harfnotu",
        )
        tree2.column("derskodu", width=268, minwidth=100, anchor=tk.CENTER)
        tree2.column("dersadi", width=268, minwidth=100, anchor=tk.CENTER)
        tree2.column("harfnotu", width=268, minwidth=100, anchor=tk.CENTER)

        tree2.heading("derskodu", text="Ders Kodu", anchor=tk.CENTER)
        tree2.heading("dersadi", text="Ders Adı", anchor=tk.CENTER)
        tree2.heading("harfnotu", text="Harf Notu", anchor=tk.CENTER)

        try:
            cursor = self.connection.cursor()
            read_query = "SELECT derskodu, dersadi, harfnotu FROM ogrencidersler WHERE sicilno = %s "
            cursor.execute(read_query, (username,))
            results = cursor.fetchall()

            i = 0
            for row in results:
                tree2.insert(
                    "",
                    i,
                    text="",
                    values=(
                        row[0],
                        row[1],
                        row[2],
                    ),
                )
                i += 1
                tree2.grid(row=2, columnspan=5)
                cursor.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Alınan Dersler Gösterilirken Hata Oluştu: ", error)
        self.disconnectToDataBase()

    # Öğrenci Listele

    def notOrtalamasi(self):
        try:
            global notOrtalamasiScreen
            notOrtalamasiScreen = Toplevel()
            notOrtalamasiScreen.title("Özel Not Ortalamaları")
            notOrtalamasiScreen.geometry("807x400")

            Label(notOrtalamasiScreen, text="Okul Numarası:").grid(row=0, column=0)
            entry = Entry(notOrtalamasiScreen)
            entry.grid(row=0, column=1)
            button = Button(
                notOrtalamasiScreen, text="ARAT", command=lambda: arat(entry.get())
            ).grid(row=0, column=2)

            def arat(username):
                self.connectToDataBase()
                cursor = self.connection.cursor()
                data_query = "SELECT derskodu FROM ogrencidersler WHERE sicilno = %s"
                cursor.execute(data_query, (username,))
                results = cursor.fetchall()
                dataDersKodu = []
                i = 0
                for i in range(len(results)):
                    dataDersKodu.append(results[i][0])
                    i += 1
                cursor.close()

                cursor = self.connection.cursor()
                data_query = "SELECT harfnotu FROM ogrencidersler WHERE sicilno = %s"
                cursor.execute(data_query, (username,))
                results = cursor.fetchall()
                dataHarfNotu = []
                j = 0
                for j in range(len(results)):
                    dataHarfNotu.append(results[j][0])
                    j += 1
                cursor.close()

                cursor = self.connection.cursor()
                data_query = "SELECT dersadi FROM ogrencidersler WHERE sicilno = %s"
                cursor.execute(data_query, (username,))
                results = cursor.fetchall()
                dataDersAdi = []
                k = 0
                for k in range(len(results)):
                    dataDersAdi.append(results[k][0])
                    k += 1
                cursor.close()

                cursor = self.connection.cursor()
                data_query = "SELECT derskodu, dersadi, harfnotu FROM ogrencidersler WHERE sicilno = %s"
                cursor.execute(data_query, (username,))
                results = cursor.fetchall()

                tree2 = ttk.Treeview(notOrtalamasiScreen)
                tree2["show"] = "headings"

                style = ttk.Style(notOrtalamasiScreen)
                style.theme_use("clam")

                tree2["columns"] = (
                    "derskodu",
                    "dersadi",
                    "harfnotu",
                )
                tree2.column("derskodu", width=268, minwidth=100, anchor=tk.CENTER)
                tree2.column("dersadi", width=268, minwidth=100, anchor=tk.CENTER)
                tree2.column("harfnotu", width=268, minwidth=100, anchor=tk.CENTER)

                tree2.heading("derskodu", text="Ders Kodu", anchor=tk.CENTER)
                tree2.heading("dersadi", text="Ders Adı", anchor=tk.CENTER)
                tree2.heading("harfnotu", text="Harf Notu", anchor=tk.CENTER)
                i = 0
                for row in results:
                    tree2.insert(
                        "",
                        i,
                        text="",
                        values=(
                            row[0],
                            row[1],
                            row[2],
                        ),
                    )
                    i += 1
                    tree2.grid(row=1, columnspan=4)
                    cursor.close()
                Label(notOrtalamasiScreen, text="Ortalamaya Ekle").grid(row=2, column=0)
                combo = ttk.Combobox(notOrtalamasiScreen, values=dataDersAdi)
                combo.set("Ders Adları")
                combo.grid(row=2, column=1)
                dersIsmi = combo.get()
                combo2 = ttk.Combobox(notOrtalamasiScreen, values=[1, 2, 3, 4])
                combo2.set("Kat Sayı")
                combo2.grid(row=2, column=2)
                dataKatSayi = []
                dataKatSayiDers = []
                dataKatSayiHarf = []
                notOrtalamaEkleButton = Button(
                    notOrtalamasiScreen, text="EKLE", command=lambda: eklemeMetod()
                )
                notOrtalamaEkleButton.grid(row=2, column=3)

                notOrtalamaHesaplaButton = Button(
                    notOrtalamasiScreen, text="HESAPLA", command=lambda: puanEkranaBas()
                )
                notOrtalamaHesaplaButton.grid(row=3, columnspan=4)

                def eklemeMetod():
                    dataKatSayi.append(combo2.get())
                    dataKatSayiDers.append(combo.get())
                    index = dataDersAdi.index(combo.get())
                    dataKatSayiHarf.append(dataHarfNotu[index])

                def hesaplaMetod():
                    toplamDers = len(dataKatSayiDers)
                    i = 0
                    toplamPuan = 0
                    for i in range(toplamDers):
                        sayisalPuan = puanHarfNotu(dataKatSayiHarf[i])
                        toplamPuan += sayisalPuan * int(dataKatSayi[i])
                        i += 1

                    toplamPuan /= toplamDers
                    return toplamPuan

                def puanHarfNotu(harfnotu):
                    if harfnotu == "AA":
                        return 4
                    elif harfnotu == "BA":
                        return 3.5
                    elif harfnotu == "BB":
                        return 3
                    elif harfnotu == "CB":
                        return 2.5
                    elif harfnotu == "CC":
                        return 2
                    elif harfnotu == "DC":
                        return 1.5
                    elif harfnotu == "DD":
                        return 1
                    elif harfnotu == "FD":
                        return 0.5
                    elif harfnotu == "FF":
                        return 0
                    else:
                        print("Geçerli Bir Değer Yollanmadı!")

                def puanEkranaBas():
                    Label(
                        notOrtalamasiScreen,
                        text=f"Öğrencinizin Puanı: {hesaplaMetod()}",
                    ).grid(row=4, columnspan=4)

                self.disconnectToDataBase()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Not Ortalaması Hesaplanırken Hata ile Karşılaşıldı: ", error)

    def manageRequests(self):
        global manageRequestScreen
        manageRequestScreen = Toplevel()
        manageRequestScreen.title("Talepleri Yönetme")
        manageRequestScreen.geometry("813x325")

        try:
            cursor = self.connection.cursor()
            read_query = "SELECT * FROM talepler"
            cursor.execute(read_query)
            results = cursor.fetchall()
            tree2 = ttk.Treeview(manageRequestScreen)
            tree2["show"] = "headings"

            style = ttk.Style(manageRequestScreen)
            style.theme_use("clam")

            tree2["columns"] = (
                "gondermezamani",
                "talepno",
                "gonderenno",
                "alicino",
                "dersismi",
                "talepsonuc",
            )
            tree2.column("gondermezamani", width=136, minwidth=100, anchor=tk.CENTER)
            tree2.column("talepno", width=35, minwidth=100, anchor=tk.CENTER)
            tree2.column("gonderenno", width=35, minwidth=100, anchor=tk.CENTER)
            tree2.column("alicino", width=35, minwidth=100, anchor=tk.CENTER)
            tree2.column("dersismi", width=150, minwidth=100, anchor=tk.CENTER)
            tree2.column("talepsonuc", width=355, minwidth=100, anchor=tk.CENTER)

            tree2.heading("gondermezamani", text="Gönderilme Zamanı", anchor=tk.CENTER)
            tree2.heading("talepno", text="Talep Numarası", anchor=tk.CENTER)
            tree2.heading("gonderenno", text="Gönderici No", anchor=tk.CENTER)
            tree2.heading("alicino", text="Alıcı No", anchor=tk.CENTER)
            tree2.heading("dersismi", text="Dersin İsmi", anchor=tk.CENTER)
            tree2.heading("talepsonuc", text="Talep Durumu", anchor=tk.CENTER)
            i = 0
            dataTalepNo = []
            for row in results:
                tree2.insert(
                    "",
                    i,
                    text="",
                    values=(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        row[5],
                    ),
                )
                dataTalepNo.append(row[1])
                i += 1
            tree2.grid(row=0, columnspan=6)
            cursor.close()

            Label(manageRequestScreen, text="Talep Onaylama - Reddetme").grid(
                row=1, column=0
            )
            combo = ttk.Combobox(manageRequestScreen, values=dataTalepNo)
            combo.set("Talep Numarası")
            combo.grid(row=1, column=1)
            onayButton = Button(
                manageRequestScreen,
                text="ONAYLA",
                command=lambda: onayMetod(combo.get()),
            )
            onayButton.grid(row=1, column=2)
            RedButton = Button(
                manageRequestScreen,
                text="REDDET",
                command=lambda: reddetMetod(combo.get()),
            )
            RedButton.grid(row=1, column=3)

            dataOgrenciler = []
            cursor = self.connection.cursor()
            ogrenci_query = "SELECT sicilno FROM ogrenciler"
            cursor.execute(ogrenci_query)
            resultsOgrenci = cursor.fetchall()

            k = 0
            for k in range(len(resultsOgrenci)):
                dataOgrenciler.append(resultsOgrenci[k])
            cursor.close()

            dataOgretmenler = []
            cursor = self.connection.cursor()
            ogretmen_query = "SELECT sicilno FROM hocalar"
            cursor.execute(ogretmen_query)
            resultsOgretmen = cursor.fetchall()

            l = 0
            for l in range(len(resultsOgretmen)):
                dataOgretmenler.append(resultsOgretmen[l])
                l += 1
            cursor.close()

            Label(manageRequestScreen, text="Öğrenciye Ders Ekle").grid(row=2, column=0)
            combo1 = ttk.Combobox(manageRequestScreen, values=dataOgrenciler)
            combo1.set("Öğrenci Numarası")
            combo1.grid(row=2, column=1, padx=5)
            combo2 = ttk.Combobox(
                manageRequestScreen, values=["Araştırma Projesi", "Bitirme Projesi"]
            )
            combo2.set("Dersin Adı")
            combo2.grid(row=2, column=2, padx=5)

            combo3 = ttk.Combobox(manageRequestScreen, values=dataOgretmenler)
            combo3.set("Öğretmen Numarası")
            combo3.grid(row=2, column=3, padx=5)

            eklemeButon = Button(
                manageRequestScreen,
                text="EKLE",
                command=lambda: addMetod(combo1.get(), combo2.get(), combo3.get()),
            ).grid(row=3, columnspan=6)

            def addMetod(ogrencino, dersadi, ogretmenno):
                self.connectToDataBase()
                try:
                    cursor = self.connection.cursor()

                    take_query = "SELECT ad FROM hocalar WHERE sicilno = %s"
                    cursor.execute(take_query, (ogretmenno,))
                    results = cursor.fetchone()
                    cursor.close()
                    cursor = self.connection.cursor()
                    take_query = "SELECT soyad FROM hocalar WHERE sicilno = %s"
                    cursor.execute(take_query, (ogretmenno,))
                    results2 = cursor.fetchone()
                    cursor.close()
                    cursor = self.connection.cursor()
                    insert_query = "INSERT INTO alinandersler (sicilno, dersadi, ogretmenad, ogretmensoyad) VALUES (%s, %s, %s, %s)"
                    cursor.execute(
                        insert_query, (ogrencino, dersadi, results[0], results2[0])
                    )
                    self.connection.commit()
                    cursor.close()
                    cursor = self.connection.cursor()
                    kontenjan_query = "UPDATE hocalar SET kontenjan = kontenjan - 1 WHERE sicilno = %s"
                    cursor.execute(kontenjan_query, (ogretmenno,))
                    self.connection.commit()
                    cursor.close()
                except (Exception, psycopg2.DatabaseError) as error:
                    print("Ders Eklenirken Hata Oluştu: ", error)
                self.disconnectToDataBase()

            def onayMetod(talepno):
                self.connectToDataBase()
                try:
                    cursor = self.connection.cursor()
                    control_query = "SELECT kontenjan FROM hocalar WHERE sicilno = (SELECT alicino FROM talepler WHERE talepno = %s)"
                    cursor.execute(control_query, (talepno,))
                    resultKontenjan = cursor.fetchone()

                    global infoScreenAccept2
                    infoScreenAccept2 = Toplevel()

                    if resultKontenjan and resultKontenjan[0] > 0:
                        cursor = self.connection.cursor()
                        accept_query = "UPDATE talepler SET talepsonuc= %s WHERE talepno = %s AND talepsonuc = %s"
                        cursor.execute(
                            accept_query, ("Onaylandı", talepno, "Değerlendirmede")
                        )
                        self.connection.commit()
                        cursor.close()

                        reduce_kontenjan_query = "UPDATE hocalar SET kontenjan = kontenjan - 1 WHERE sicilno = (SELECT alicino FROM talepler WHERE talepno = %s)"
                        cursor = self.connection.cursor()
                        cursor.execute(reduce_kontenjan_query, (talepno,))
                        self.connection.commit()
                        cursor.close()

                        cursor = self.connection.cursor()
                        read_query = (
                            "SELECT talepsonuc FROM talepler WHERE talepno = %s"
                        )
                        cursor.execute(read_query, (talepno,))
                        result = cursor.fetchone()
                        cursor.close()

                        if result and result[0] == "Onaylandı":
                            infoScreenAccept2.title("Talep Kabul Edildi!")
                            Label(
                                infoScreenAccept2,
                                text="Talebi Başarıyla Kabul Ettiniz!",
                            ).grid(row=0, column=0)
                            Button(
                                infoScreenAccept2,
                                text="Tamam",
                                command=lambda: infoScreenAccept2.withdraw(),
                            ).grid(row=1, column=0)
                            infoScreenAccept2.deiconify()
                        else:
                            infoScreenAccept2.title(
                                "Talep Kabul Edilirken Hata Oluştu!"
                            )
                            Label(
                                infoScreenAccept2,
                                text="Lütfen Geçerli Bir Talep Numarası Giriniz!",
                            ).grid(row=0, column=0)
                            Button(
                                infoScreenAccept2,
                                text="Tamam",
                                command=lambda: infoScreenAccept2.withdraw(),
                            ).grid(row=1, column=0)
                            infoScreenAccept2.deiconify()
                    else:
                        infoScreenAccept2.title("Kontenjan Yetersiz!")
                        Label(
                            infoScreenAccept2,
                            text="Kontenjanınız Dolu! Lütfen Yöneticiniz ile İletişime Geçiniz!",
                        ).grid(row=0, column=0)
                        Button(
                            infoScreenAccept2,
                            text="Tamam",
                            command=lambda: infoScreenAccept2.withdraw(),
                        ).grid(row=1, column=0)
                        infoScreenAccept2.deiconify()

                except (Exception, psycopg2.DatabaseError) as error:
                    print("Talep Kabul Edilirken Hata ile Karşılaşıldı: ", error)
                self.disconnectToDataBase()

            def reddetMetod(talepno):
                self.connectToDataBase()
                try:
                    cursor = self.connection.cursor()
                    reject_query = "UPDATE talepler SET talepsonuc = %s WHERE talepno = %s AND talepsonuc = %s"
                    cursor.execute(
                        reject_query, ("Reddedildi", talepno, "Değerlendirmede")
                    )
                    self.connection.commit()
                    cursor.close()

                    cursor = self.connection.cursor()
                    read_query = "SELECT talepsonuc FROM talepler WHERE talepno = %s"
                    cursor.execute(read_query, (talepno,))
                    result = cursor.fetchone()

                    global infoScreenReject
                    infoScreenReject = Toplevel()
                    if result and result[0] == "Reddedildi":
                        infoScreenReject.title("Talep Reddedildi!")
                        Label(
                            infoScreenReject, text="Talebi Başarıyla Reddettiniz!"
                        ).grid(row=0, column=0)
                        Button(
                            infoScreenReject,
                            text="Tamam",
                            command=lambda: infoScreenReject.withdraw(),
                        ).grid(row=1, column=0)
                        infoScreenReject.deiconify()
                    else:
                        infoScreenReject.title("Reddedilirken Hata Oluştu!")
                        Label(
                            infoScreenReject,
                            text="Lütfen Geçerli Bir Talep Numarası Giriniz!",
                        ).grid(row=0, column=0)
                        Button(
                            infoScreenReject,
                            text="Tamam",
                            command=lambda: infoScreenReject.withdraw(),
                        ).grid(row=1, column=0)
                        infoScreenReject.deiconify()
                except (Exception, psycopg2.DatabaseError) as error:
                    print("Talep Reddedilirken Hata ile Karşılaşıldı: ", error)
                self.disconnectToDataBase()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Talepler Yönetilirken Hata İle Karşılaşıldı: ", error)

    def randomStudentGenerator(self, sayi):
        sayi = int(sayi)
        self.connectToDataBase()
        try:
            i = 0
            ogrenciAd = []
            ogrenciSoyad = []
            ogrenciSifre = []
            ogrenciGPA = []
            sicilNolar = []
            for i in range(sayi):
                ogrenciAd.append(f"ad{i}")
                ogrenciSoyad.append(f"soyad{i}")
                ogrenciSifre.append(f"sifre{i}")
                ortalama = i % 4
                ogrenciGPA.append(ortalama)
                i += 1
            cursor = self.connection.cursor()
            insert_query = "INSERT INTO kullanicilar (ad, soyad, sifre, tur) VALUES (%s, %s, %s, %s)"
            for j in range(sayi):
                cursor.execute(
                    insert_query,
                    (ogrenciAd[j], ogrenciSoyad[j], ogrenciSifre[j], "ogrenci"),
                )
                self.connection.commit()

            read_query = "SELECT sicilno FROM kullanicilar WHERE ad = %s AND soyad = %s AND sifre = %s AND tur = %s "
            for k in range(sayi):
                cursor.execute(
                    read_query,
                    (ogrenciAd[k], ogrenciSoyad[k], ogrenciSifre[k], "ogrenci"),
                )
                result = cursor.fetchone()
                sicilNolar.append(result[0])

            cursor.close()

            cursor = self.connection.cursor()
            insert_query = "INSERT INTO ogrenciler (sicilno, ad, soyad, gpa, aldigiderssayisi) VALUES (%s, %s, %s, %s, %s)"
            for m in range(sayi):
                cursor.execute(
                    insert_query,
                    (sicilNolar[m], ogrenciAd[m], ogrenciSoyad[m], ogrenciGPA[m], 0),
                )
                self.connection.commit()

            cursor.close()

            cursor = self.connection.cursor()
            read_query = "SELECT derskodu, dersadi, harfnotu FROM ogrencidersler WHERE sicilno = 12"
            cursor.execute(read_query)
            results = cursor.fetchall()

            row1 = 0
            dersKodlari = []
            dersAdlari = []
            harfNotlari = []
            for row1 in range(len(results)):
                dersKodlari.append(results[row1][0])
                dersAdlari.append(results[row1][1])
                row1 += 1

            row1 = 0
            for row1 in range(len(dersKodlari)):
                randomS = random.randint(1, 9)
                if randomS == 1:
                    harfNotlari.append("AA")
                elif randomS == 2:
                    harfNotlari.append("BA")
                elif randomS == 3:
                    harfNotlari.append("BB")
                elif randomS == 4:
                    harfNotlari.append("CB")
                elif randomS == 5:
                    harfNotlari.append("CC")
                elif randomS == 6:
                    harfNotlari.append("DC")
                elif randomS == 7:
                    harfNotlari.append("DD")
                elif randomS == 8:
                    harfNotlari.append("FD")
                elif randomS == 9:
                    harfNotlari.append("FF")
                else:
                    print("Random Yapılamadı!")
                row1 += 1
            cursor.close()

            cursor = self.connection.cursor()
            insert_query = "INSERT INTO ogrencidersler (sicilno, derskodu, dersadi, harfnotu) VALUES (%s, %s, %s, %s)"
            s = 0
            t = 0
            for t in range(sayi):
                for s in range(len(dersKodlari)):
                    cursor.execute(
                        insert_query,
                        (
                            sicilNolar[t],
                            dersKodlari[s],
                            dersAdlari[s],
                            harfNotlari[s],
                        ),
                    )
                    s += 1
                t += 1
            self.connection.commit()
            cursor.close()

        except ValueError as error:
            print("Rastgele Öğrenci Oluşturulurken Hata Oluştu: ", error)
        self.disconnectToDataBase()

    def randomAtama(self):
        ogrenciler = self.showFreeStudents()
        ogretmenlerSicilNo = []
        ogretmenlerAd = []
        ogretmenlerSoyad = []
        dersler = ["Araştırma Projesi", "Bitirme Projesi"]
        try:
            cursor = self.connection.cursor()
            data_query = "SELECT sicilno FROM hocalar WHERE kontenjan > 0"
            cursor.execute(data_query)
            results = cursor.fetchall()
            k = 0
            for k in range(len(results)):
                ogretmenlerSicilNo.append(results[k])
                k += 1
            cursor.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Öğretmenler Çekilirken Hata Oluştu", error)

        i = 0
        secilenOgretmenler = []
        for i in range(len(ogrenciler)):
            randomS = random.randint(0, len(ogretmenlerSicilNo) - 1)
            secilenOgretmenler.append(ogretmenlerSicilNo[randomS])
            i += 1

        try:
            cursor = self.connection.cursor()
            query = "SELECT ad FROM hocalar WHERE sicilno= %s"
            query1 = "SELECT soyad FROM hocalar WHERE sicilno= %s"
            i = 0
            for i in range(len(secilenOgretmenler)):
                cursor.execute(query, (secilenOgretmenler[i],))
                result = cursor.fetchone()
                ogretmenlerAd.append(result[0])
                i += 1
            cursor.close()

            cursor = self.connection.cursor()
            for i in range(len(secilenOgretmenler)):
                cursor.execute(query1, (secilenOgretmenler[i],))
                result = cursor.fetchone()
                ogretmenlerSoyad.append(result[0])
                i += 1
            cursor.close()
        except (ValueError, psycopg2.DatabaseError) as error:
            print("Öğretmenler Atanırken Hata Oluştu: ", error)

        try:
            cursor = self.connection.cursor()
            insert_query = "INSERT INTO alinandersler (sicilno, dersadi, ogretmenad, ogretmensoyad) VALUES (%s, %s, %s, %s)"
            i = 0
            for i in range(len(ogrenciler)):
                j = 0
                for j in range(2):
                    cursor.execute(
                        insert_query,
                        (
                            ogrenciler[i],
                            dersler[j],
                            ogretmenlerAd[i],
                            ogretmenlerSoyad[i],
                        ),
                    )
                    j += 1
                i += 1
            self.connection.commit()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Öğretmen Atanırken Hata Oluştu: ", error)


if __name__ == "__main__":
    connect = ConnectionToDatabase()
    connect.randomAtama()
    connect.disconnectToDataBase()
