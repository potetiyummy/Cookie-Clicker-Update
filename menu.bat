@echo off
echo どれを購入しますか？

echo 1. クリック力を上げる (30クッキー)
echo 2. 自動クリック (100クッキー)

set /p num=選択肢を入力してください:

if "%num%"=="1" (
    echo クリック力UPシグナルを送信しました。
    echo 1 > menu_tmp\upgrade.txt
) else if "%num%"=="2" (
    echo 自動クリックONシグナルを送信しました。
    echo 2 > menu_tmp\upgrade.txt
) else (
    echo 無効な選択肢です。
)

echo このウィンドウを安全に閉じることができます。ゲームに戻るには、このウィンドウを閉じてください。