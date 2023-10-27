from pathlib import Path
from tkinter import *
import postgresql

OUTPUT_PATH_LOGIN = Path(__file__).parent
ASSETS_PATH_LOGIN = OUTPUT_PATH_LOGIN / Path(
    r"/Users/veliashvili/Desktop/YazLab/assetsLoginPanel/frame0"
)

OUTPUT_PATH_ADMIN = Path(__file__).parent
ASSETS_PATH_ADMIN = OUTPUT_PATH_ADMIN / Path(
    r"/Users/veliashvili/Desktop/YazLab/assetsAdminPanel/frame0"
)

# SQL connect item
global connect
connect = postgresql.ConnectionToDatabase()


def relative_to_assets_login(path: str) -> Path:
    return ASSETS_PATH_LOGIN / Path(path)


def relative_to_assets_admin(path: str) -> Path:
    return ASSETS_PATH_ADMIN / Path(path)


def login():
    username = entryLoginScreenUsername.get()
    password = entryLoginScreenPassword.get()

    if connect.login(username, password):
        user_type = connect.whoIsLogin(username)
        if user_type == "admin":
            main_frame.pack_forget()
            admin_frame.pack(fill="both", expand=True)
            connect.disconnectToDataBase()
        elif user_type == "ogretmen":
            pass  # Öğretmen Ekranına Geçişin Kodlanması
        elif user_type == "ogrenci":
            pass  # Öğrenci Ekranına Geçişin Kodlanması
    else:
        global errorScreen
        errorScreen = Toplevel()
        errorScreen.title("Hatalı Giriş")
        errorScreen.geometry("200x60")
        Label(errorScreen, text="Kullanıcı Adı veya Şifre Hatalı!").grid(row=0)
        Button(errorScreen, text="Tamam", command=lambda: errorScreen.withdraw()).grid(
            row=1
        )
        errorScreen.deiconify()


def hocaEkle():
    hocaAd = entryAdminScreenHocaAd.get()
    hocaSoyad = entryAdminScreenHocaSoyad.get()
    hocaSifre = entryAdminScreenhocaSifre.get()
    hocaIlgiAlani = entryAdminScreenHocaIlgi.get()
    hocaKota = entryAdminScreenHocaKota.get()

    connect.connectToDataBase()
    connect.insertTeacher(hocaAd, hocaSoyad, hocaSifre, hocaKota, hocaIlgiAlani)
    connect.disconnectToDataBase()


def ogrenciEke():
    ogrenciAd = entryAdminScreenOgrenciAd.get()
    ogrenciSoyad = entryAdminScreenOgrenciSoyad.get()
    ogrenciSifre = entryAdminScreenOgrenciSifre.get()
    ogrenciNot = entryAdminScreenOgrenciNot.get()
    ogrenciDersSayi = entryAdminScreenOgrenciDersSayi.get()

    connect.connectToDataBase()
    connect.insertStudents(
        ogrenciAd, ogrenciSoyad, ogrenciSifre, ogrenciNot, ogrenciDersSayi
    )
    connect.disconnectToDataBase()


def kullaniciSil():
    kullaniciNo = entryAdminScreenSilme.get()
    connect.connectToDataBase()
    user_type = connect.whoIsLogin(kullaniciNo)

    if user_type == "ogretmen":
        connect.deleteTeacher(kullaniciNo)
    elif user_type == "ogrenci":
        connect.deleteStudent(kullaniciNo)
    elif user_type == "admin":
        global errorScreenDelete
        errorScreenDelete = Toplevel()
        errorScreenDelete.title("Yönetici Silinemez!")
        errorScreenDelete.geometry("200x60")
        Label(errorScreenDelete, text="Yönetici Silinemez!").grid(row=0)
        Button(
            errorScreenDelete,
            text="Tamam",
            command=lambda: errorScreenDelete.withdraw(),
        ).grid(row=1)
        errorScreenDelete.deiconify()

    connect.disconnectToDataBase()


def ogrenciBilgileriAl():
    connect.connectToDataBase()
    connect.readStudent()
    connect.disconnectToDataBase()


def ogretmenBilgileriAl():
    connect.connectToDataBase()
    connect.readTeacher()
    connect.disconnectToDataBase()


def kullaniciBilgiGuncelle():
    kullaniciNo = entryAdminScreenGuncelle.get()
    connect.connectToDataBase()
    user_type = connect.whoIsLogin(kullaniciNo)
    userName = connect.whoIsLoginName(kullaniciNo)

    if user_type == "admin":
        global errorScreenUpdate
        errorScreenUpdate = Toplevel()
        errorScreenUpdate.title("Yönetici Bilgileri Değiştirilemez!")
        errorScreenUpdate.geometry("200x60")
        Label(errorScreenUpdate, text="Yönetici Bilgileri Değiştirilemez!").grid(row=0)
        Button(
            errorScreenUpdate,
            text="Tamam",
            command=lambda: errorScreenUpdate.withdraw(),
        ).grid(row=1)
        errorScreenUpdate.deiconify()
    elif user_type == "ogrenci":
        global updateScreenStudent
        updateScreenStudent = Toplevel()
        updateScreenStudent.title("Öğrenci Bilgilerini Güncelleme")
        updateScreenStudent.geometry("310x170")

        Label(updateScreenStudent, text=userName.upper()).grid(row=0, columnspan=2)

        Label(updateScreenStudent, text="Ad").grid(row=1, column=0)
        updateOgrenciAd = Entry(updateScreenStudent)
        updateOgrenciAd.grid(row=1, column=1)

        Label(updateScreenStudent, text="Soyad").grid(row=2, column=0)
        updateOgrenciSoyad = Entry(updateScreenStudent)
        updateOgrenciSoyad.grid(row=2, column=1)

        Label(updateScreenStudent, text="Not Ortalaması").grid(row=3, column=0)
        updateOgrenciNotOrtalama = Entry(updateScreenStudent)
        updateOgrenciNotOrtalama.grid(row=3, column=1)

        Label(updateScreenStudent, text="Aldığı Ders Sayısı").grid(row=4, column=0)
        updateOgrenciAlinanDers = Entry(updateScreenStudent)
        updateOgrenciAlinanDers.grid(row=4, column=1)

        Button(
            updateScreenStudent,
            text="Güncelle",
            command=lambda: ogrenciBilgiGuncelle(
                kullaniciNo,
                updateOgrenciAd.get(),
                updateOgrenciSoyad.get(),
                updateOgrenciNotOrtalama.get(),
                updateOgrenciAlinanDers.get(),
            ),
        ).grid(row=5, columnspan=2)
    elif user_type == "ogretmen":
        global updateScreenTeacher
        updateScreenTeacher = Toplevel()
        updateScreenTeacher.title("Öğretmen Bilgilerini Güncelleme")
        updateScreenTeacher.geometry("310x170")

        Label(updateScreenTeacher, text=userName.upper()).grid(row=0, columnspan=2)

        Label(updateScreenTeacher, text="Ad").grid(row=1, column=0)
        updateOgretmenAd = Entry(updateScreenTeacher)
        updateOgretmenAd.grid(row=1, column=1)

        Label(updateScreenTeacher, text="Soyad").grid(row=2, column=0)
        updateOgretmenSoyad = Entry(updateScreenTeacher)
        updateOgretmenSoyad.grid(row=2, column=1)

        Label(updateScreenTeacher, text="Kontenjan").grid(row=3, column=0)
        updateOgretmenKontenjan = Entry(updateScreenTeacher)
        updateOgretmenKontenjan.grid(row=3, column=1)

        Label(updateScreenTeacher, text="İlgi Alanı").grid(row=4, column=0)
        updateOgretmenIlgiAlani = Entry(updateScreenTeacher)
        updateOgretmenIlgiAlani.grid(row=4, column=1)

        Button(
            updateScreenTeacher,
            text="Güncelle",
            command=lambda: ogretmenBilgiGuncelle(
                kullaniciNo,
                updateOgretmenAd.get(),
                updateOgretmenSoyad.get(),
                updateOgretmenKontenjan.get(),
                updateOgretmenIlgiAlani.get(),
            ),
        ).grid(row=5, columnspan=2)


def ogrenciBilgiGuncelle(
    sicilNo, yeniAd, yeniSoyad, yeniNotOrtalama, yeniAldigiDersSayi
):
    connect.connectToDataBase()
    connect.updateStudent(
        sicilNo, yeniAd, yeniSoyad, yeniNotOrtalama, yeniAldigiDersSayi
    )
    connect.disconnectToDataBase()


def ogretmenBilgiGuncelle(sicilNo, yeniAd, yeniSoyad, yeniKontenjan, yeniIlgiAlani):
    connect.connectToDataBase()
    connect.updateTeacher(sicilNo, yeniAd, yeniSoyad, yeniKontenjan, yeniIlgiAlani)
    connect.disconnectToDataBase()


window = Tk()

window.geometry("1366x768")
window.configure(bg="#FFFFFF")

main_frame = Frame(window, bg="#FFFFFF")
main_frame.pack(fill="both", expand=True)

admin_frame = Frame(window, bg="#FFFFFF")

##################### LOGIN SCREEN ############################

canvasLoginScreen = Canvas(
    main_frame,
    bg="#FFFFFF",
    height=768,
    width=1366,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)

canvasLoginScreen.place(x=0, y=0)
canvasLoginScreen.create_rectangle(0.0, 0.0, 1366.0, 768.0, fill="#F1EEEE", outline="")

entryLoginScreenUsername_image_1 = PhotoImage(
    file=relative_to_assets_login("entryLoginScreen1.png")
)
entryLoginScreenUsername_bg_1 = canvasLoginScreen.create_image(
    913.5, 300.0, image=entryLoginScreenUsername_image_1
)
entryLoginScreenUsername = Entry(
    main_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryLoginScreenUsername.place(x=768.0, y=270.0, width=291.0, height=58.0)

entryLoginScreenPassword_image_2 = PhotoImage(
    file=relative_to_assets_login("entryLoginScreen2.png")
)
entryLoginScreenPassword_bg_2 = canvasLoginScreen.create_image(
    913.5, 461.0, image=entryLoginScreenPassword_image_2
)
entryLoginScreenPassword = Entry(
    main_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0, show="*"
)
entryLoginScreenPassword.place(x=768.0, y=431.0, width=291.0, height=58.0)

canvasLoginScreen.create_rectangle(0.0, 0.0, 1366.0, 138.0, fill="#00A571", outline="")

KOU_Logo_image = PhotoImage(file=relative_to_assets_login("KouLogo.png"))
KOU_Logo = canvasLoginScreen.create_image(160.0, 69.0, image=KOU_Logo_image)

loginScreenWelcomeLabel = Label(
    main_frame,
    text="KOCAELİ ÜNİVERSİTESİ DERS SEÇİM SİSTEMİNE HOŞ GELDİNİZ!",
    bg="#00A571",
    fg="#FFFFFF",
    font=("Inter", 30),
)
loginScreenWelcomeLabel.place(x=289, y=44, anchor="nw")

loginScreenUserIdLabel = Label(
    main_frame, text="Kullanıcı Adı", bg="#F1EEEE", fg="#000000", font=("Inter", 30)
)
loginScreenUserIdLabel.place(x=332, y=270, anchor="nw")

loginScreenPasswordLabel = Label(
    main_frame, text="Şifre", bg="#F1EEEE", fg="#000000", font=("Inter", 30)
)
loginScreenPasswordLabel.place(x=332, y=431, anchor="nw")

LoginScreenButtonImage = PhotoImage(file=relative_to_assets_login("LoginButton.png"))
LoginScreenButton = Button(
    main_frame,
    image=LoginScreenButtonImage,
    borderwidth=0,
    highlightthickness=0,
    command=login,
    relief="flat",
)
LoginScreenButton.place(x=469.0, y=592.0, width=445.0, height=82.0)

##################### LOGIN SCREEN END ############################


##################### ADMIN SCREEN ############################

canvasAdminScreen = Canvas(
    admin_frame,
    bg="#FFFFFF",
    height=768,
    width=1366,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)

canvasAdminScreen.place(x=0, y=0)
canvasAdminScreen.create_rectangle(0.0, 0.0, 1366.0, 768.0, fill="#F1EEEE", outline="")

adminScreenDersSecimLabel = Label(
    admin_frame,
    text="Ders Seçim Süresi",
    bg="#F1EEEE",
    fg="#000000",
    font=("Inter", 15),
)
adminScreenDersSecimLabel.place(x=32, y=317, anchor="nw")

adminScreenMesajKarakterLabel = Label(
    admin_frame,
    text="Mesaj Karakter Sayısı",
    bg="#F1EEEE",
    fg="#000000",
    font=("Inter", 15),
)
adminScreenMesajKarakterLabel.place(x=30, y=372, anchor="nw")

adminScreenOgrenciAtaLabel = Label(
    admin_frame, text="Öğrencileri Ata", bg="#F1EEEE", fg="#000000", font=("Inter", 15)
)
adminScreenOgrenciAtaLabel.place(x=34, y=451, anchor="nw")

adminScreenOgrenciBilgileriLabel = Label(
    admin_frame,
    text="Öğrenci Bilgileri",
    bg="#F1EEEE",
    fg="#000000",
    font=("Inter", 15),
)
adminScreenOgrenciBilgileriLabel.place(x=32, y=541, anchor="nw")

adminScreenOgretmenBilgileriLabel = Label(
    admin_frame,
    text="Öğretmen Bilgileri",
    bg="#F1EEEE",
    fg="#000000",
    font=("Inter", 15),
)
adminScreenOgretmenBilgileriLabel.place(x=364, y=536, anchor="nw")

adminScreenHocaKisitLabel = Label(
    admin_frame,
    text="Hoca Kısıtlama Durumu",
    bg="#F1EEEE",
    fg="#000000",
    font=("Inter", 15),
)
adminScreenHocaKisitLabel.place(x=765, y=452, anchor="nw")

adminScreenOkulNoLabel = Label(
    admin_frame, text="Okul Numarası", bg="#F1EEEE", fg="#000000", font=("Inter", 15)
)
adminScreenOkulNoLabel.place(x=738, y=536, anchor="nw")

adminScreenOkulNo2Label = Label(
    admin_frame, text="Okul Numarası", bg="#F1EEEE", fg="#000000", font=("Inter", 15)
)
adminScreenOkulNo2Label.place(x=708, y=378, anchor="nw")

adminScreenHocaSayiKacLabel = Label(
    admin_frame, text="Kaç Farklı Hoca", bg="#F1EEEE", fg="#000000", font=("Inter", 15)
)
adminScreenHocaSayiKacLabel.place(x=702, y=322, anchor="nw")

adminScreenIlgiAlanLabel = Label(
    admin_frame, text="İlgi Alanı", bg="#F1EEEE", fg="#000000", font=("Inter", 20)
)
adminScreenIlgiAlanLabel.place(x=820, y=167, anchor="nw")

adminScreenGPALabel = Label(
    admin_frame, text="GPA", bg="#F1EEEE", fg="#000000", font=("Inter", 20)
)
adminScreenGPALabel.place(x=820, y=240, anchor="nw")

adminScreenSoyadLabel = Label(
    admin_frame, text="Soyad", bg="#F1EEEE", fg="#000000", font=("Inter", 20)
)
adminScreenSoyadLabel.place(x=428, y=167, anchor="nw")

adminScreenSoyad2Label = Label(
    admin_frame, text="Soyad", bg="#F1EEEE", fg="#000000", font=("Inter", 20)
)
adminScreenSoyad2Label.place(x=428, y=242, anchor="nw")

adminScreenSifreLabel = Label(
    admin_frame, text="Şifre", bg="#F1EEEE", fg="#000000", font=("Inter", 20)
)
adminScreenSifreLabel.place(x=643, y=167, anchor="nw")

adminScreenSifre2Label = Label(
    admin_frame, text="Şifre", bg="#F1EEEE", fg="#000000", font=("Inter", 20)
)
adminScreenSifre2Label.place(x=643, y=240, anchor="nw")

adminScreenAdLabel = Label(
    admin_frame, text="Ad", bg="#F1EEEE", fg="#000000", font=("Inter", 20)
)
adminScreenAdLabel.place(x=254, y=167, anchor="nw")

adminScreenAd2Label = Label(
    admin_frame, text="Ad", bg="#F1EEEE", fg="#000000", font=("Inter", 20)
)
adminScreenAd2Label.place(x=254, y=242, anchor="nw")

adminScreenHocaEkleLabel = Label(
    admin_frame, text="Hoca Ekle", bg="#F1EEEE", fg="#000000", font=("Inter", 15)
)
adminScreenHocaEkleLabel.place(x=31, y=193, anchor="nw")

adminScreenOgrenciEkleLabel = Label(
    admin_frame, text="Öğrenci Ekle", bg="#F1EEEE", fg="#000000", font=("Inter", 15)
)
adminScreenOgrenciEkleLabel.place(x=31, y=253, anchor="nw")

canvasAdminScreen.create_rectangle(0.0, 0.0, 1366.0, 138.0, fill="#00A571", outline="")

adminKouLogoImage = PhotoImage(file=relative_to_assets_admin("KouLogo1.png"))
adminKouLogo = canvasAdminScreen.create_image(160.0, 69.0, image=adminKouLogoImage)

adminScreenWelcomeLabel = Label(
    admin_frame,
    text="YÖNETİCİ PANELİNE HOŞ GELDİNİZ!",
    bg="#00A571",
    fg="#FFFFFF",
    font=("Inter", 30),
)
adminScreenWelcomeLabel.place(x=439, y=44, anchor="nw")

entryAdminScreen_image_1 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen1.png")
)
entryAdminScreen_bg_1 = canvasAdminScreen.create_image(
    268.0, 208.5, image=entryAdminScreen_image_1
)
entryAdminScreenHocaAd = Entry(
    admin_frame,
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
)
entryAdminScreenHocaAd.place(x=193.0, y=193.0, width=150.0, height=29.0)

entryAdminScreen_image_2 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen2.png")
)
entryAdminScreen_bg_2 = canvasAdminScreen.create_image(
    268.0, 281.5, image=entryAdminScreen_image_2
)
entryAdminScreenOgrenciAd = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreenOgrenciAd.place(x=193.0, y=266.0, width=150.0, height=29.0)

entryAdminScreen_image_3 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen3.png")
)
entryAdminScreen_bg_3 = canvasAdminScreen.create_image(
    294.0, 334.5, image=entryAdminScreen_image_3
)
entryAdminScreenDersSec = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreenDersSec.place(x=194.0, y=319.0, width=200.0, height=29.0)

entryAdminScreen_image_4 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen4.png")
)
entryAdminScreen_bg_4 = canvasAdminScreen.create_image(
    294.0, 390.5, image=entryAdminScreen_image_4
)
entryAdminScreenMesajKarakter = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreenMesajKarakter.place(x=194.0, y=375.0, width=200.0, height=29.0)

entryAdminScreen_image_5 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen5.png")
)
entryAdminScreen_bg_5 = canvasAdminScreen.create_image(
    993.0, 334.5, image=entryAdminScreen_image_5
)
entryAdminScreenKacHoca = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreenKacHoca.place(x=893.0, y=319.0, width=200.0, height=29.0)

entryAdminScreen_image_6 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen6.png")
)
entryAdminScreen_bg_6 = canvasAdminScreen.create_image(
    993.0, 390.5, image=entryAdminScreen_image_6
)
entryAdminScreenSilme = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreenSilme.place(x=893.0, y=375.0, width=200.0, height=29.0)

entryAdminScreen_image_7 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen7.png")
)
entryAdminScreen_bg_7 = canvasAdminScreen.create_image(
    996.0, 551.5, image=entryAdminScreen_image_7
)
entryAdminScreenGuncelle = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreenGuncelle.place(x=896.0, y=536.0, width=200.0, height=29.0)

entryAdminScreen_image_8 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen8.png")
)
entryAdminScreen_bg_8 = canvasAdminScreen.create_image(
    469.0, 210.5, image=entryAdminScreen_image_8
)
entryAdminScreenHocaSoyad = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreenHocaSoyad.place(x=394.0, y=195.0, width=150.0, height=29.0)

entryAdminScreen_image_9 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen9.png")
)
entryAdminScreen_bg_9 = canvasAdminScreen.create_image(
    469.0, 283.5, image=entryAdminScreen_image_9
)
entryAdminScreenOgrenciSoyad = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreenOgrenciSoyad.place(x=394.0, y=268.0, width=150.0, height=29.0)

entryAdminScreen_image_10 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen10.png")
)
entryAdminScreen_bg_10 = canvasAdminScreen.create_image(
    667.0, 210.5, image=entryAdminScreen_image_10
)
entryAdminScreenhocaSifre = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreenhocaSifre.place(x=592.0, y=195.0, width=150.0, height=29.0)

entryAdminScreen_image_11 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen11.png")
)
entryAdminScreen_bg_11 = canvasAdminScreen.create_image(
    667.0, 281.5, image=entryAdminScreen_image_11
)
entryAdminScreenOgrenciSifre = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreenOgrenciSifre.place(x=592.0, y=266.0, width=150.0, height=29.0)

entryAdminScreen_image_12 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen12.png")
)
entryAdminScreen_bg_12 = canvasAdminScreen.create_image(
    865.0, 208.5, image=entryAdminScreen_image_12
)
entryAdminScreenHocaIlgi = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreenHocaIlgi.place(x=790.0, y=193.0, width=150.0, height=29.0)

entryAdminScreen_image_13 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen13.png")
)
entryAdminScreen_bg_13 = canvasAdminScreen.create_image(
    865.0, 281.5, image=entryAdminScreen_image_13
)
entryAdminScreenOgrenciNot = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreenOgrenciNot.place(x=790.0, y=266.0, width=150.0, height=29.0)

entryAdminScreen_image_14 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen14.png")
)
entryAdminScreen_bg_14 = canvasAdminScreen.create_image(
    1063.0, 208.5, image=entryAdminScreen_image_14
)
entryAdminScreenHocaKota = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreenHocaKota.place(x=988.0, y=193.0, width=150.0, height=29.0)

entryAdminScreen_image_15 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen15.png")
)
entryAdminScreen_bg_15 = canvasAdminScreen.create_image(
    1063.0, 282.5, image=entryAdminScreen_image_15
)
entryAdminScreenOgrenciDersSayi = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreenOgrenciDersSayi.place(x=988.0, y=267.0, width=150.0, height=29.0)

AdminScreenButton1Image = PhotoImage(
    file=relative_to_assets_admin("adminScreenButton1.png")
)
AdminScreenButton1 = Button(
    admin_frame,
    image=AdminScreenButton1Image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: hocaEkle(),
    relief="flat",
)
AdminScreenButton1.place(x=1182.0, y=193.0, width=150.0, height=31.0)

loginScreenButton2Image = PhotoImage(
    file=relative_to_assets_admin("loginScreenButton2.png")
)
loginScreenButton2 = Button(
    admin_frame,
    image=loginScreenButton2Image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat",
)
loginScreenButton2.place(x=1134.0, y=323.0, width=200.0, height=31.0)

adminScreenButton3Image = PhotoImage(
    file=relative_to_assets_admin("adminScreenButton3.png")
)
adminScreenButtonKullaniciSil = Button(
    admin_frame,
    image=adminScreenButton3Image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: kullaniciSil(),
    relief="flat",
)
adminScreenButtonKullaniciSil.place(x=1132.0, y=375.0, width=200.0, height=31.0)

adminScreenButton4Image = PhotoImage(
    file=relative_to_assets_admin("adminScreenButton4.png")
)
adminScreenButtonKullaniciBilgiGuncelle = Button(
    admin_frame,
    image=adminScreenButton4Image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: kullaniciBilgiGuncelle(),
    relief="flat",
)
adminScreenButtonKullaniciBilgiGuncelle.place(
    x=1133.0, y=536.0, width=200.0, height=31.0
)

loginScreenButton5Image = PhotoImage(
    file=relative_to_assets_admin("loginScreenButton5.png")
)
loginScreenButton5 = Button(
    admin_frame,
    image=loginScreenButton5Image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat",
)
loginScreenButton5.place(x=968.0, y=448.0, width=170.0, height=31.0)

loginScreenButton6Image = PhotoImage(
    file=relative_to_assets_admin("loginScreenButton6.png")
)
loginScreenButton6 = Button(
    admin_frame,
    image=loginScreenButton6Image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_6 clicked"),
    relief="flat",
)
loginScreenButton6.place(x=1164.0, y=448.0, width=170.0, height=31.0)

loginScreenButton7Image = PhotoImage(
    file=relative_to_assets_admin("loginScreenButton7.png")
)
loginScreenButton7 = Button(
    admin_frame,
    image=loginScreenButton7Image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_7 clicked"),
    relief="flat",
)
loginScreenButton7.place(x=428.0, y=319.0, width=200.0, height=31.0)

loginScreenButton8Image = PhotoImage(
    file=relative_to_assets_admin("loginScreenButton8.png")
)
loginScreenButton8 = Button(
    admin_frame,
    image=loginScreenButton8Image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_8 clicked"),
    relief="flat",
)
loginScreenButton8.place(x=428.0, y=376.0, width=200.0, height=31.0)

loginScreenButton9Image = PhotoImage(
    file=relative_to_assets_admin("loginScreenButton9.png")
)
loginScreenButton9 = Button(
    admin_frame,
    image=loginScreenButton9Image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_9 clicked"),
    relief="flat",
)
loginScreenButton9.place(x=163.0, y=448.0, width=170.0, height=31.0)

adminScreenButton10Image = PhotoImage(
    file=relative_to_assets_admin("adminScreenButton10.png")
)
adminScreenButtonOgrenciBilgiAl = Button(
    admin_frame,
    image=adminScreenButton10Image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ogrenciBilgileriAl(),
    relief="flat",
)
adminScreenButtonOgrenciBilgiAl.place(x=171.0, y=536.0, width=170.0, height=31.0)

adminScreenButton11Image = PhotoImage(
    file=relative_to_assets_admin("adminScreenButton11.png")
)
adminScreenButtonHocaBilgileriAl = Button(
    admin_frame,
    image=adminScreenButton11Image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ogretmenBilgileriAl(),
    relief="flat",
)
adminScreenButtonHocaBilgileriAl.place(x=532.0, y=536.0, width=170.0, height=31.0)

loginScreenButton12Image = PhotoImage(
    file=relative_to_assets_admin("loginScreenButton12.png")
)
loginScreenButton12 = Button(
    admin_frame,
    image=loginScreenButton12Image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_12 clicked"),
    relief="flat",
)
loginScreenButton12.place(x=534.0, y=618.0, width=300.0, height=31.0)

loginScreenButton13Image = PhotoImage(
    file=relative_to_assets_admin("loginScreenButton13.png")
)
loginScreenButton13 = Button(
    admin_frame,
    image=loginScreenButton13Image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_13 clicked"),
    relief="flat",
)
loginScreenButton13.place(x=1004.0, y=618.0, width=300.0, height=31.0)

loginScreenButton14Image = PhotoImage(
    file=relative_to_assets_admin("loginScreenButton14.png")
)
loginScreenButton14 = Button(
    admin_frame,
    image=loginScreenButton14Image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_14 clicked"),
    relief="flat",
)
loginScreenButton14.place(x=64.0, y=618.0, width=300.0, height=31.0)

loginScreenButton15Image = PhotoImage(
    file=relative_to_assets_admin("loginScreenButton15.png")
)
loginScreenButton15 = Button(
    admin_frame,
    image=loginScreenButton15Image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_15 clicked"),
    relief="flat",
)
loginScreenButton15.place(x=565.0, y=448.0, width=170.0, height=31.0)

loginScreenButton16Image = PhotoImage(
    file=relative_to_assets_admin("loginScreenButton16.png")
)
loginScreenButton16 = Button(
    admin_frame,
    image=loginScreenButton16Image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_16 clicked"),
    relief="flat",
)
loginScreenButton16.place(x=370.0, y=448.0, width=170.0, height=31.0)

adminScreenButton17Image = PhotoImage(
    file=relative_to_assets_admin("adminScreenButton17.png")
)
adminScreenButtonOgrenciEkle = Button(
    admin_frame,
    image=adminScreenButton17Image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ogrenciEke(),
    relief="flat",
)
adminScreenButtonOgrenciEkle.place(x=1182.0, y=267.0, width=150.0, height=31.0)

adminScreenKontenjanLabel = Label(
    admin_frame, text="Kontenjan", bg="#F1EEEE", fg="#000000", font=("Inter", 20)
)
adminScreenKontenjanLabel.place(x=1014, y=163, anchor="nw")

adminScreenDersSayisiLabel = Label(
    admin_frame, text="Ders Sayısı", bg="#F1EEEE", fg="#000000", font=("Inter", 20)
)
adminScreenDersSayisiLabel.place(x=1004, y=239, anchor="nw")

canvasAdminScreen.create_rectangle(
    31.0, 238.0, 1331.999755859375, 239.63537883758545, fill="#878282", outline=""
)

canvasAdminScreen.create_rectangle(
    31.0, 309.0, 1331.9993896484375, 311.27074432373047, fill="#878282", outline=""
)

canvasAdminScreen.create_rectangle(
    31.0, 423.7747344970703, 1331.99951171875, 426.0, fill="#878282", outline=""
)

canvasAdminScreen.create_rectangle(
    31.0, 501.0, 1333.99951171875, 503.0, fill="#878282", outline=""
)

canvasAdminScreen.create_rectangle(
    31.0, 591.0, 1334.0, 592.0000305175781, fill="#878282", outline=""
)

canvasAdminScreen.create_rectangle(
    31.0, 680.9999694824219, 1337.99951171875, 683.0, fill="#878282", outline=""
)

canvasAdminScreen.create_rectangle(
    33.0, 361.0, 1333.9993896484375, 363.27073669433594, fill="#878282", outline=""
)

adminScreenKOULabel = Label(
    admin_frame,
    text="KOCAELİ ÜNİVERSİTESİ",
    bg="#F1EEEE",
    fg="#000000",
    font=("Inter", 20),
)
adminScreenKOULabel.place(x=69, y=725, anchor="nw")

adminScreenMeteLabel = Label(
    admin_frame, text="METEHAN BELLİ", bg="#F1EEEE", fg="#000000", font=("Inter", 20)
)
adminScreenMeteLabel.place(x=1168, y=725, anchor="nw")

##################### ADMIN SCREEN END ############################

window.resizable(False, False)
window.mainloop()
