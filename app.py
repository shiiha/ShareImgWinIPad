from __future__ import annotations

from datetime import datetime
from pathlib import Path
from uuid import uuid4

from flask import Flask, jsonify, render_template, request, send_file
from PIL import Image

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
LATEST_FILE = DATA_DIR / "latest.png"
META_FILE = DATA_DIR / "latest.txt"

app = Flask(__name__)
DATA_DIR.mkdir(exist_ok=True)


def _normalize_to_png(src: Path, dst: Path) -> None:
    with Image.open(src) as img:
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA")
        img.save(dst, format="PNG", optimize=True)


@app.get("/")
def index():
    has_image = LATEST_FILE.exists()
    updated_at = META_FILE.read_text(encoding="utf-8").strip() if META_FILE.exists() else ""
    return render_template("index.html", has_image=has_image, updated_at=updated_at)


@app.get("/latest-image")
def latest_image():
    if not LATEST_FILE.exists():
        return jsonify({"error": "画像はまだ送信されていません"}), 404
    return send_file(LATEST_FILE, mimetype="image/png")


@app.post("/upload")
def upload_image():
    upload = request.files.get("image")
    if upload is None:
        return jsonify({"error": "image フィールドがありません"}), 400

    temp_name = f"upload-{uuid4()}.bin"
    temp_path = DATA_DIR / temp_name
    upload.save(temp_path)

    try:
        _normalize_to_png(temp_path, LATEST_FILE)
    except Exception as exc:  # pragma: no cover - input file validation
        temp_path.unlink(missing_ok=True)
        return jsonify({"error": f"画像として処理できません: {exc}"}), 400

    temp_path.unlink(missing_ok=True)
    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    META_FILE.write_text(updated_at, encoding="utf-8")
    return jsonify({"status": "ok", "updated_at": updated_at})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8787, debug=False)
