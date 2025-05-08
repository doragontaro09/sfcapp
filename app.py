from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

# CSVファイル名
CSV_FILE = "sfc_list.csv"

# CSVを読み込んでゲームリストを返す関数
def load_games():
    with open(CSV_FILE, mode='r', encoding='utf-8-sig') as f:  # BOM付き対応
        reader = csv.DictReader(f)
        games = []
        for row in reader:
            clean_row = {
                "タイトル": row.get("タイトル", "").strip(),
                "メーカー": row.get("メーカー", "").strip(),
                "発売日": row.get("発売日", "").strip(),
                "ジャンル": row.get("ジャンル", "").strip(),
                "価格": row.get("価格", "").strip(),
                "備考": row.get("備考", "").strip(),
                "所持": row.get("所持", row.get("〇", "")).strip()
            }
            games.append(clean_row)
        return games




# ゲームリストをCSVに保存する関数
def save_games(games):
    with open(CSV_FILE, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=games[0].keys())
        writer.writeheader()
        writer.writerows(games)

# ホーム画面（一覧・検索表示）
@app.route("/")
def index():
    games = load_games()
    query = request.args.get("q", default="")
    if query:
        filtered = [(i, g) for i, g in enumerate(games) if query in g['タイトル']]
    else:
        filtered = list(enumerate(games))
    return render_template("index.html", games=filtered, query=query)

# 所持状態の切り替え
@app.route("/toggle")
def toggle():
    index = request.args.get("index")
    if index is None:
        return redirect(url_for("index"))
    try:
        idx = int(index)
        games = load_games()
        current = games[idx]['所持']
        games[idx]['所持'] = '×' if current == '〇' else '〇'
        save_games(games)
    except:
        pass
    return redirect(url_for("index"))

# アプリ起動
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


