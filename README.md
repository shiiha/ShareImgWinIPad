# ShareImgWinIPad

Windows の右クリックから画像を送信し、iPad ですぐ貼り付けられる状態（クリップボード）にするための最小構成です。

## 仕組み
1. Windows で画像を右クリックして「iPadへ送る」。
2. PowerShell が画像をローカルサーバーにアップロード。
3. iPad で Web ページを開き「画像をコピー」を押す。
4. iPad 側の任意アプリでペースト。

## セットアップ（PC）
```bash
python -m venv .venv
source .venv/bin/activate  # Windowsなら .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

サーバーは `0.0.0.0:8787` で起動します。iPad からは `http://<PCのIP>:8787` にアクセスしてください。

## Windows 右クリック導入
1. `scripts/send_to_ipad.ps1` を例えば `C:\ShareImgWinIPad\send_to_ipad.ps1` に配置。
2. `scripts/install_context_menu.ps1` の `YOUR-PC-IP` をPCのIPに変更。
3. 管理者 PowerShell で `install_context_menu.ps1` を実行。

これで画像ファイル右クリックメニューに「iPadへ送る」が追加されます。

## iPad での利用
- Safari で `http://<PCのIP>:8787` を開く。
- 「画像をコピー」を押す。
- メモ、LINE、Pages など貼り付け先アプリでペースト。

## 注意点
- iOS/Safari は Clipboard API 制限があるため、環境によっては **HTTPS** が必要です。
- 社内Wi-FiやゲストWi-Fiでは端末間通信が遮断される場合があります。
