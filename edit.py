import pandas as pd
import openpyxl
import os

#files=エクセルファイルが格納されている変数
def edit(files):
    print('sono1')
    print(files)
    #データフレーム形式に変換
    edit_df = pd.read_excel('static/csv')
    print('sono2')
    print(edit_df)
    #パスを作成
    edit_file_path = 'download/' + 'csv' + '_result.xlsx'
    print('sono3')
    print(edit_file_path)
    #作成したパスにエクセルファイルを保存
    edit_df.to_excel(edit_file_path)
    print('sono4')
    workbook = openpyxl.load_workbook(edit_file_path)
    print('sono5')
    print(workbook)
    worksheet = workbook.worksheets[0]
    print('sono6')
    print(worksheet)

    #処理を保存
    workbook.save(edit_file_path)

    #パスを返す
    return edit_file_path[9:]
