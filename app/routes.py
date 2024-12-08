from flask import Blueprint, render_template, request
import pandas as pd
import os

bp = Blueprint('main', __name__)

DATA_FILE = "data.csv"

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = request.form['date']
        subject = request.form['subject']
        topic = request.form['topic']
        status = request.form['status']

        # データを保存
        if not os.path.exists(DATA_FILE):
            df = pd.DataFrame(columns=["Date", "Subject", "Topic", "Status"])
        else:
            df = pd.read_csv(DATA_FILE)

        # 新しい行を DataFrame に追加
        new_row = pd.DataFrame([{"Date": date, "Subject": subject, "Topic": topic, "Status": status}])
        df = pd.concat([df, new_row], ignore_index=True)

        # CSV に保存
        df.to_csv(DATA_FILE, index=False)

        return render_template('index.html', message="データを保存しました！")

    return render_template('index.html', message="")
@bp.route('/table')
def table():
    if not os.path.exists(DATA_FILE):  # ファイルがない場合
        return render_template('table.html', data={})

    df = pd.read_csv(DATA_FILE)

    # CSVファイルが空の場合のチェック
    if df.empty:
        return render_template('table.html', data={})

    # 教科ごとに「できた」「できなかった」を分類
    grouped_data = {}
    for subject, group in df.groupby('Subject'):
        grouped_data[subject] = {
            "できた": group[group["Status"] == "できた"]["Topic"].tolist(),
            "できなかった": group[group["Status"] == "できなかった"]["Topic"].tolist()
        }

    return render_template('table.html', data=grouped_data)