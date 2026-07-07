#ライブラリ読み込み
import tkinter as tk,os,time as tm,sys,json as jn,random as rd,math as mt,subprocess as sp,threading as th;from PIL import Image as im, ImageTk as itk;from tkinter import messagebox as mb;import signal as sg

root = tk.Tk();root.state('zoomed');root.title("Cookie Clicker");root.configure(bg="#156a89") #rootの設定

save_file = "savedata.json" #セーブデータの保存先

if os.path.exists(save_file): #スコアロード
    with open(save_file, "r", encoding="utf-8") as f:
        data = jn.load(f)
        score = data.get("score", 0)
else:
    score = 0

# ↓ 変数定義 ↓ 
SCALE_FACTOR = 8;scorelavel = tk.Label(root, text=f"スコア: {str(score)}", font=("Arial", 24), bg="#156a89");scorelavel.pack(pady=20);cookie = tk.Canvas(root, width=300, height=300, highlightthickness=0, bg="#156a89");cookie.pack(pady=20);new_cookie_width = im.open("cookie.png").width * SCALE_FACTOR;new_cookie_height = im.open("cookie.png").height * SCALE_FACTOR;large_cookie_img = im.open("cookie.png").resize((new_cookie_width, new_cookie_height), im.NEAREST);tk_large_cookie_img = itk.PhotoImage(large_cookie_img);menu = tk.Canvas(root, width=300, height=300, highlightthickness=0, bg="#156a89");menu.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20);menu_img = im.open("menu.png");large_menu_img = menu_img.resize((menu_img.width * 8, menu_img.height * 8), im.NEAREST);tk_large_menu_img = itk.PhotoImage(large_menu_img);image_id = menu.create_image(150, 150, image=tk_large_menu_img, anchor=tk.CENTER)

if os.path.exists(save_file): #その他のデータロード
    with open(save_file, "r", encoding="utf-8") as f:
        data = jn.load(f) #データをロード
        oneclick_power = data.get("oneclick_power", 1) #クリック力を取得
        auto_click = data.get("auto_click", False) #自動クリックの真偽値を取得
        auto_click_power = data.get("auto_click_power", 1) #自動クリックパワーを取得
        oneclick_power_upgrade_cost = data.get("oneclick_power_upgrade_cost", 30) #クリック力UPのアップグレードのコストを取得
        auto_click_upgrade_cost = data.get("auto_click_upgrade_cost", 100)

oneclick_power_up = oneclick_power*1.5 #次回のアップグレード時のクリック力の倍率

def on_menu_click(event): #メニューclick処理
    sp.Popen(["start", "menu.bat"], shell=True)
    
    while not os.path.exists("menu_tmp\\upgrade.txt"):
        tm.sleep(0.5)
    if os.path.exists("menu_tmp\\upgrade.txt"):
        with open("menu_tmp\\upgrade.txt", "r", encoding="utf-8") as f:
            content = f.read()
    else:
        mb.showerror("エラー", "アップグレード情報の取得に失敗しました。もう一度メニューからアップグレードを行ってください。")
    content_len = len(content)
    if content_len > 0:
        int_content = int(content)
        if int_content == 1: #クリック力UP
            global oneclick_power, oneclick_power_up, score
            
            if score >= oneclick_power_upgrade_cost: #コスト・スコア判定
                oneclick_power *= oneclick_power_up
                mb.showinfo("アップグレード完了", f"クリック力が{oneclick_power_up}倍になりました！\n現在のクリック力: {oneclick_power}")
            else:
                mb.showerror("スコアが足りません!", f'あと必要なコストは{oneclick_power_upgrade_cost - score}です！')
        elif int_content == 2:
            global auto_click, auto_click_power
            if score >= auto_click_upgrade_cost:
                auto_click = True
                auto_click_power += 1
                mb.showinfo("アップグレード完了", f"自動クリックが有効になりました！\n現在の自動クリック力: {auto_click_power}")
            else:
                mb.showerror("スコアが足りません!", f'あと必要なコストは{auto_click_upgrade_cost - score}です！')
    else: #エラー
        mb.showerror("エラー", "アップグレード情報の取得に失敗しました。もう一度メニューからアップグレードを行ってください。")
    os.remove("menu_tmp\\upgrade.txt")
            
def move_particle(particle, dx, dy, gravity): #パーティクル処理
    cookie.move(particle, dx, dy)
    dy += gravity
    coords = cookie.coords(particle)
    if coords and coords[1] < root.winfo_height():
        root.after(20, lambda: move_particle(particle, dx, dy, gravity))
    else:
        cookie.delete(particle)

def on_cookie_click(event): #クッキーclick処理
    global score
    score += oneclick_power
    scorelavel.config(text=f"スコア: {str(score)}")
    for _ in range(3):
        px = event.x + rd.randint(-10, 10)
        py = event.y + rd.randint(-10, 10)
        size = rd.randint(4, 8)
        
        color = rd.choice(["#8B4513", "#A0522D", "#CD853F"])
        
        particle = cookie.create_oval(px, py, px+size, py+size, fill=color, outline="")
        
        dx = rd.uniform(-3, 3)
        dy = rd.uniform(-5, -2)
        gravity = 0.3
        
        move_particle(particle, dx, dy, gravity)

def auto_click_function(): #自動クリック処理
    global score, auto_click, auto_click_power
    while True:
        if auto_click:
            score += auto_click_power
            scorelavel.config(text=f"スコア: {str(score)}")
            tm.sleep(1)

def data_save_function(): #データ保存処理
    global score, oneclick_power, auto_click, auto_click_power
    data = {
            "score": score,
            "oneclick_power": oneclick_power,
            "auto_click": auto_click,
            "auto_click_power" : auto_click_power
        }
    with open(save_file, "w", encoding="utf-8") as f:
        jn.dump(data, f, ensure_ascii=False, indent=4)

def auto_save_function(): #自動保存処理
    while True:
        data_save_function()
        tm.sleep(1)

def handler(signum, frame):
    pass

auto_click_thread = th.Thread(target=auto_click_function, daemon=True) # 自動クリックスレッド開始
auto_click_thread.start()

auto_save_thread = th.Thread(target=auto_save_function, daemon=True) # 自動保存スレッド開始
auto_save_thread.start()

if tk_large_cookie_img: #クッキーの画像をクリック可能にする
    image_obj_id = cookie.create_image(150, 150, image=tk_large_cookie_img, anchor=tk.CENTER)
    cookie.tag_bind(image_obj_id, "<Button-1>", on_cookie_click)
    cookie.tag_bind(image_obj_id, "<Enter>", lambda e: cookie.config(cursor="hand2"))
if tk_large_menu_img: #メニューの画像をクリック可能にする
    image_obj_id = menu.create_image(150, 150, image=tk_large_menu_img, anchor=tk.CENTER)
    menu.tag_bind(image_obj_id, "<Button-1>", on_menu_click)

sg.signal(sg.SIGINT, handler)

root.mainloop() #起動