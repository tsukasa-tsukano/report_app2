from flask import Flask, render_template, session, request, redirect, url_for
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask import send_from_directory
from edit import edit

#インスタンスの作成
app = Flask(__name__)

#暗号鍵の作成
key = os.urandom(21)
app.secret_key = key

#データベース設定
#データベースのURIを代入
URI = 'postgresql://postgres:D7Kd8Qr5@localhost/report_db2'
#インスタンスであるappに設定を追加する。データベースの変更の警告を無効化
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#作成したURIを代入
app.config['SQLALCHEMY_DATABASE_URI'] = URI
#データベースを操作する機能にFlaskインスタンスを渡してデータベースをインスタンス化
db = SQLAlchemy(app)

#テーブル内の設定
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), index=True, unique=True)
    file_path = db.Column(db.String(64), index=True, unique=True)
    dt = db.Column(db.DateTime, nullable=False, default=datetime.now)


#テーブルの初期化
@app.cli.command('initdb')
def initdb():
    db.create_all()

#メイン
@app.route("/")
def index():
    #データベースに登録されているデータをすべて取り出す
    data = Data.query.all()
    #表示させたいdataを渡す
    return render_template('index.html',data=data)

#ファイルアップロード
@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/register', methods=['POST'])
def register():
    #upload.htmlで入力されたタイトル名を取り出す
    title = request.form['title']
    #ファイルを取り出す
    f = request.files['file']
    #セキュリティの観点からファイル名を適当に変える。ファイルをstaticディレクトリに保存する
    file_path = 'static/' + secure_filename(f.filename)
    f.save(file_path)

    #取り出したタイトル名と作成したfile_pathを渡してインスタンス化
    registered_file = Data(title=title, file_path=file_path)
    #データベースに追加
    db.session.add(registered_file)
    #データベースに登録
    db.session.commit()

    return redirect(url_for('index'))

#GETメソッドでIDが送信されてくるのでこのように記述。intで整数型に変換
@app.route('/delete/<int:id>', methods=['GET'])
#delete関数に引数idを与える
def delete(id):
    #データベースから該当するデータを取得
    data = Data.query.get(id)
    #staticフォルダからも削除するためfile_pathを取得
    delete_file = data.file_path
    #データベースに登録する手順と逆の処理
    db.session.delete(data)
    db.session.commit()
    #staticディレクトリから該当ファイルを削除
    os.remove(delete_file)
    #処理を終えたらトップページに返す
    return redirect(url_for('index'))

@app.route('/edit', methods=["POST"])
def edit_files():
    print('sono1')
    #データベースからExcelファイルのパスを取り出してまとめる空のリスト
    files = []
    print('sono2')
    data = Data.query.all()
    print('sono3')
    print(data)
    files.append(data[-1].file_path)
    print('sono4')
    print(files)
    #file_pathが格納されたリストをedit_file()関数に渡す
    edit_file_path = edit(files)
    print('sono5')
    print(edit_file_path)
    #downloadディレクトリから、pred_file()関数で生成されたExcelファイルを返す
    return send_from_directory('download', edit_file_path, as_attachment=True)
    print('sono6')


#アプリケーションの起動
if __name__ == '__main__':
    app.run(debug=True)
