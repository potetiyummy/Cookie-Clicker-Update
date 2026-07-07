import tkinter as tk
import os
import random
import json
import requests
from PIL import Image as im, ImageTk as itk 

SCALE_FACTOR = 8

URL_API_CONTENTS = "https://api.github.com/repos/potetiyummy/Cookie-Clicker-Update/contents/"
FILE_SHA_MANIFEST = "sha_manifest.json"

def sync_assets():
    print("アセットの更新・破損チェック中...")
    local_sha_data = {}
    if os.path.exists(FILE_SHA_MANIFEST):
        try:
            with open(FILE_SHA_MANIFEST, "r", encoding="utf-8") as f:
                local_sha_data = json.load(f)
        except Exception:
            pass
            
    try:
        res_contents = requests.get(URL_API_CONTENTS, timeout=5)
        if res_contents.status_code != 200:
            print("GitHubからの情報取得に失敗しました。オフラインモードで起動します。")
            return
            
        github_files = res_contents.json()
        updated_sha_data = {}
        has_changes = False

        for file_info in github_files:
            if file_info["type"] == "file":
                file_name = file_info["name"]
                remote_sha = file_info["sha"]
                download_url = file_info["download_url"]

                updated_sha_data[file_name] = remote_sha

                if local_sha_data.get(file_name) != remote_sha or not os.path.exists(file_name):
                    print(f"更新または破損を検知: {file_name} をダウンロード中...")
                    res_file = requests.get(download_url, timeout=10)
                    if res_file.status_code == 200:
                        with open(file_name, "wb") as f:
                            f.write(res_file.content)
                        has_changes = True
                    else:
                        print(f"{file_name} の取得に失敗しました。")
                else:

                    updated_sha_data[file_name] = local_sha_data[file_name]

        if has_changes or not os.path.exists(FILE_SHA_MANIFEST):
            with open(FILE_SHA_MANIFEST, "w", encoding="utf-8") as f:
                json.dump(updated_sha_data, f, indent=2, ensure_ascii=False)
            print("アセットの同期が完了しました！")
        else:
            print("すべて最新の状態です。")
            
    except Exception as e:
        print(f"同期中にエラーが発生しました: {e}")

sync_assets()