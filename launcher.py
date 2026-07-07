import os
import subprocess
import tkinter as tk;from tkinter import messagebox
from PIL import Image as im, ImageTk as itk

root = tk.Tk()
root.title("Cookie Clicker Launcher")

# --- ★ここから中央配置の処理 ---
WINDOW_WIDTH = 1560
WINDOW_HEIGHT = 1020

# 画面全体のサイズを取得
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 中央に置くための開始座標を計算
x = (screen_width // 2) - (WINDOW_WIDTH // 2)
y = (screen_height // 2) - (WINDOW_HEIGHT // 2)

# ジオメトリを設定 (例: "1200x600+360+240")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
# ------------------------------

# 画像の読み込み（前と同じ）
pil_img = im.open("launcher.png")
tk_img = itk.PhotoImage(pil_img)
imglavel = tk.Label(root, image=tk_img)
imglavel.image = tk_img
imglavel.pack()

FILE_SHA_MANIFEST = "sha_manifest.json"
FILE_GAME = "game.py"
FILE_COOKIE = "cookie.png"
FILE_UPDATER = "update.py"

def launch_sequence():
    """起動チェックを行い、違いがあればアップデートするかプレイヤーに確認する"""
    is_missing = (
        not os.path.exists(FILE_GAME) or 
        not os.path.exists(FILE_COOKIE) or 
        not os.path.exists(FILE_SHA_MANIFEST)
    )
    
    if is_missing:
        # そもそもファイルが足りない場合は、事故ではないので自動で修復を入れる
        print("必要なファイルが不足しています。自動修復を開始します...")
        run_updater_and_start()
    else:
        # ファイルは揃っているが、GitHub側に新しい更新があるかを仮チェック
        # (update.pyを呼び出す前にランチャー側で確認するか、一回update.pyに確認させる)
        # 今回は「常に最新か確認ダイアログを出す」か、あるいは「安全に手動選択させる」形にします。
        
        # 💡 事故防止用の確認ダイアログを表示
        answer = messagebox.askyesno(
            "アップデートの確認", 
            "GitHub上の最新バージョンを確認し、必要であればアップデート（上書き）しますか？\n\n"
            "※『いいえ』を選ぶと、現在PCにあるファイルのままゲームを起動します（スキップ）。"
        )
        
        if answer: # 「はい」を選んだ場合
            print("アップデートを確認します...")
            run_updater_and_start()
        else: # 「いいえ」を選んだ場合（スキップ）
            print("アップデートをスキップしました。現行ファイルで起動します。")
            start_game_directly()

def run_updater_and_start():
    """update.pyを実行してゲームを起動し、ランチャーを閉じる"""
    if os.path.exists(FILE_UPDATER):
        subprocess.run(["python", FILE_UPDATER])
        if os.path.exists(FILE_GAME):
            subprocess.Popen(["python", FILE_GAME])
    else:
        print("エラー: 修復プログラム（update.py）が見つかりません。")
        # update.pyがなくても一応game.pyがあれば起動を試みる
        start_game_directly()
    
    close_launcher()

def start_game_directly():
    """update.pyを挟まずに直接game.pyを起動する"""
    if os.path.exists(FILE_GAME):
        subprocess.Popen(["python", FILE_GAME])
    else:
        print("エラー: game.py が見つかりません。")
    close_launcher()

def close_launcher():
    """ランチャー画面を完全に閉じる"""
    root.quit()
    root.destroy()

# 画面が表示された後にチェックを開始
root.after(100, launch_sequence)
root.mainloop()