import psycopg2
from config import config
import tkinter as tk
from tkinter import ttk, Toplevel, Label, Entry, Button
from PyPDF2 import PdfReader
import re


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

if __name__ == "__main__":
    connect = ConnectionToDatabase()
    # print(connect.showFreeStudents())
    connect.dersBilgiGetir(24)
    connect.disconnectToDataBase()
