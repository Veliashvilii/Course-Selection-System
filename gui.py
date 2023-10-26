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
        user_type = connect.whoIsLogin(username, password)
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
    text="Öğreretmen Bilgileri",
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
entryAdminScreen1 = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreen1.place(x=193.0, y=193.0, width=150.0, height=29.0)

entryAdminScreen_image_2 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen2.png")
)
entryAdminScreen_bg_2 = canvasAdminScreen.create_image(
    268.0, 281.5, image=entryAdminScreen_image_2
)
entryAdminScreen2 = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreen2.place(x=193.0, y=266.0, width=150.0, height=29.0)

entryAdminScreen_image_3 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen3.png")
)
entryAdminScreen_bg_3 = canvasAdminScreen.create_image(
    294.0, 334.5, image=entryAdminScreen_image_3
)
entryAdminScreen3 = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreen3.place(x=194.0, y=319.0, width=200.0, height=29.0)

entryAdminScreen_image_4 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen4.png")
)
entryAdminScreen_bg_4 = canvasAdminScreen.create_image(
    294.0, 390.5, image=entryAdminScreen_image_4
)
entryAdminScreen4 = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreen4.place(x=194.0, y=375.0, width=200.0, height=29.0)

entryAdminScreen_image_5 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen5.png")
)
entryAdminScreen_bg_5 = canvasAdminScreen.create_image(
    993.0, 334.5, image=entryAdminScreen_image_5
)
entryAdminScreen5 = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreen5.place(x=893.0, y=319.0, width=200.0, height=29.0)

entryAdminScreen_image_6 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen6.png")
)
entryAdminScreen_bg_6 = canvasAdminScreen.create_image(
    993.0, 390.5, image=entryAdminScreen_image_6
)
entryAdminScreen6 = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreen6.place(x=893.0, y=375.0, width=200.0, height=29.0)

entryAdminScreen_image_7 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen7.png")
)
entryAdminScreen_bg_7 = canvasAdminScreen.create_image(
    996.0, 551.5, image=entryAdminScreen_image_7
)
entryAdminScreen7 = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreen7.place(x=896.0, y=536.0, width=200.0, height=29.0)

entryAdminScreen_image_8 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen8.png")
)
entryAdminScreen_bg_8 = canvasAdminScreen.create_image(
    469.0, 210.5, image=entryAdminScreen_image_8
)
entryAdminScreen8 = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreen8.place(x=394.0, y=195.0, width=150.0, height=29.0)

entryAdminScreen_image_9 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen9.png")
)
entryAdminScreen_bg_9 = canvasAdminScreen.create_image(
    469.0, 283.5, image=entryAdminScreen_image_9
)
entryAdminScreen9 = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreen9.place(x=394.0, y=268.0, width=150.0, height=29.0)

entryAdminScreen_image_10 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen10.png")
)
entryAdminScreen_bg_10 = canvasAdminScreen.create_image(
    667.0, 210.5, image=entryAdminScreen_image_10
)
entryAdminScreen10 = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreen10.place(x=592.0, y=195.0, width=150.0, height=29.0)

entryAdminScreen_image_11 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen11.png")
)
entryAdminScreen_bg_11 = canvasAdminScreen.create_image(
    667.0, 281.5, image=entryAdminScreen_image_11
)
entryAdminScreen11 = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreen11.place(x=592.0, y=266.0, width=150.0, height=29.0)

entryAdminScreen_image_12 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen12.png")
)
entryAdminScreen_bg_12 = canvasAdminScreen.create_image(
    865.0, 208.5, image=entryAdminScreen_image_12
)
entryAdminScreen12 = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreen12.place(x=790.0, y=193.0, width=150.0, height=29.0)

entryAdminScreen_image_13 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen13.png")
)
entryAdminScreen_bg_13 = canvasAdminScreen.create_image(
    865.0, 281.5, image=entryAdminScreen_image_13
)
entryAdminScreen13 = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreen13.place(x=790.0, y=266.0, width=150.0, height=29.0)

entryAdminScreen_image_14 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen14.png")
)
entryAdminScreen_bg_14 = canvasAdminScreen.create_image(
    1063.0, 208.5, image=entryAdminScreen_image_14
)
entryAdminScreen14 = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreen14.place(x=988.0, y=193.0, width=150.0, height=29.0)

entryAdminScreen_image_15 = PhotoImage(
    file=relative_to_assets_admin("entryAdminScreen15.png")
)
entryAdminScreen_bg_15 = canvasAdminScreen.create_image(
    1063.0, 282.5, image=entryAdminScreen_image_15
)
entryAdminScreen15 = Entry(
    admin_frame, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0
)
entryAdminScreen15.place(x=988.0, y=267.0, width=150.0, height=29.0)

loginScreenButton1Image = PhotoImage(
    file=relative_to_assets_admin("loginScreenButton1.png")
)
loginScreenButton1 = Button(
    admin_frame,
    image=loginScreenButton1Image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat",
)
loginScreenButton1.place(x=1182.0, y=193.0, width=150.0, height=31.0)

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

loginScreenButton3Image = PhotoImage(
    file=relative_to_assets_admin("loginScreenButton3.png")
)
loginScreenButton3 = Button(
    admin_frame,
    image=loginScreenButton3Image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat",
)
loginScreenButton3.place(x=1132.0, y=375.0, width=200.0, height=31.0)

loginScreenButton4Image = PhotoImage(
    file=relative_to_assets_admin("loginScreenButton4.png")
)
loginScreenButton4 = Button(
    admin_frame,
    image=loginScreenButton4Image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat",
)
loginScreenButton4.place(x=1133.0, y=536.0, width=200.0, height=31.0)

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

loginScreenButton10Image = PhotoImage(
    file=relative_to_assets_admin("loginScreenButton10.png")
)
loginScreenButton10 = Button(
    admin_frame,
    image=loginScreenButton10Image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_10 clicked"),
    relief="flat",
)
loginScreenButton10.place(x=171.0, y=536.0, width=170.0, height=31.0)

loginScreenButton11Image = PhotoImage(
    file=relative_to_assets_admin("loginScreenButton11.png")
)
loginScreenButton11 = Button(
    admin_frame,
    image=loginScreenButton11Image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_11 clicked"),
    relief="flat",
)
loginScreenButton11.place(x=532.0, y=536.0, width=170.0, height=31.0)

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

loginScreenButton17Image = PhotoImage(
    file=relative_to_assets_admin("loginScreenButton17.png")
)
loginScreenButton17 = Button(
    admin_frame,
    image=loginScreenButton17Image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_17 clicked"),
    relief="flat",
)
loginScreenButton17.place(x=1182.0, y=267.0, width=150.0, height=31.0)

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
