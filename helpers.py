import os
import csv
from datetime import date
from itertools import chain

import pandas as pd
import mysql.connector as mysql

from constatns import file_titles, files as source


def get_products(file_name: str) -> dict:
    directory = source[file_name]
    files = os.listdir(directory)
    options = []

    files.sort(key=lambda x: os.path.getctime(os.path.join(directory, x)), reverse=True)

    last_file_path = os.path.join(directory, files[0])
    df = pd.read_csv(last_file_path)

    for index, row in df.iterrows():
        product = row["Product"]
        sku = row["SKU"]
        options.append({"sku": sku, "product": product, "file_name": file_name})

    return {"script": file_titles[file_name], "options": options}


def get_product_by_sku(file_name: str, sku: str):
    directory = source[file_name]
    files = os.listdir(directory)
    files.sort(key=lambda x: os.path.getctime(os.path.join(directory, x)), reverse=True)

    last_file_path = os.path.join(directory, files[0])
    df = pd.read_csv(last_file_path)

    return dict(df[df["SKU"] == sku].iloc[0])


def lerCSV():
    arquivoCSV = pd.read_csv('2023_02_10_Setec.csv', index_col=False, delimiter=",")
    arquivoCSV.head()
    print(arquivoCSV)

def getConnection():
    conn = mysql.connect(host='localhost', database='csv',
                         user='root', password='root')
    return conn

def getExistingSkus():
    conn = getConnection()
    sql_stm = "SELECT SKU FROM zalihi"
    cursor = conn.cursor()
    cursor.execute(sql_stm)
    records = cursor.fetchall()
    existing_skus = list(chain(*records))
    cursor.close()
    return existing_skus

def insertCsvToMySQL():

    conn = getConnection()

    existing_skus = getExistingSkus()

    with open("data/output.csv", 'r', encoding="utf8") as arquivoCSV:
        dadosCSV = csv.reader(arquivoCSV, delimiter=",")
        dadosToMySQL = []
        updateStockValues = []
        for row in dadosCSV:
            currentSku = int(row[57])
            if not currentSku in existing_skus:
                dadosToMySQL.append((row[57], row[0], row[2], row[3], row[5], row[6], row[7], row[9], row[10], row[16], row[17], row[18], row[45], date.today()))
            else:
                updateStockValues.append((row[9], row[57]))

        cur = conn.cursor()
        sql_stm = "INSERT INTO zalihi (SKU,Category,Product,Variant,Price,OldPrice,Currency,Stock,Units,Annotation,Description,Images,Garancija,DataImport) value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.executemany(sql_stm,dadosToMySQL)

        sql_stm_update = "UPDATE zalihi SET Stock = %s WHERE SKU = %s"
        cur.executemany(sql_stm_update, updateStockValues)

        conn.commit()
        cur.close()

if __name__ == '__main__':
    insertCsvToMySQL()
