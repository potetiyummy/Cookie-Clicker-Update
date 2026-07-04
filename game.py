import tkinter as tk,os,time as tm,sys,json as jn,random as rd,math as mt
from PIL import Image as im, ImageTk as itk 

root = tk.Tk()
root.state('zoomed')
root.title("Cookie Clicker")
root.configure(bg="#156a89")

score = 0

SCALE_FACTOR = 8


scorelavel = tk.Label(root, text=f"スコア: {str(score)}", font=("Arial", 24), bg="#156a89")
scorelavel.pack(pady=20)
cookie = tk.Canvas(root, width=300, height=300, highlightthickness=0, bg="#156a89")
cookie.pack(pady=20)
new_cookie_width = im.open("cookie.png").width * SCALE_FACTOR
new_cookie_height = im.open("cookie.png").height * SCALE_FACTOR
large_cookie_img = im.open("cookie.png").resize((new_cookie_width, new_cookie_height), im.NEAREST)
tk_large_cookie_img = itk.PhotoImage(large_cookie_img)

def move_particle(particle, dx, dy, gravity):
    cookie.move(particle, dx, dy)
    dy += gravity
    coords = cookie.coords(particle)
    if coords and coords[1] < root.winfo_height():
        root.after(20, lambda: move_particle(particle, dx, dy, gravity))
    else:
        cookie.delete(particle)

def on_cookie_click(event):
    global score
    score += 1
    scorelavel.config(text=f"スコア: {str(score)}")
    for _ in range(3):
        # クリックされた位置（event.x, event.y）の近くに小さな円を作る
        px = event.x + rd.randint(-10, 10)
        py = event.y + rd.randint(-10, 10)
        size = rd.randint(4, 8)  # 破片の大きさ
        
        # クッキーっぽい茶色のグラデーションをランダムで選択
        color = rd.choice(["#8B4513", "#A0522D", "#CD853F"])
        
        # 破片（円）をCanvas上に作成
        particle = cookie.create_oval(px, py, px+size, py+size, fill=color, outline="")
        
        # 飛び散る速度をランダムに設定（上や左右にちょっと跳ねてから落ちる）
        dx = rd.uniform(-3, 3)
        dy = rd.uniform(-5, -2)
        gravity = 0.3  # 重力の強さ
        
        # 破片のアニメーションを開始！
        move_particle(particle, dx, dy, gravity)

if tk_large_cookie_img:
    image_obj_id = cookie.create_image(150, 150, image=tk_large_cookie_img, anchor=tk.CENTER)
    cookie.tag_bind(image_obj_id, "<Button-1>", on_cookie_click)
    cookie.tag_bind(image_obj_id, "<Enter>", lambda e: cookie.config(cursor="hand2"))

root.mainloop()