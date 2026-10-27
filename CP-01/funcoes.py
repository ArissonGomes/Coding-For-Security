# Este arquivo tem funções que seram utilizadas nos exercícios
import mysql.connector
import os
from mysql.connector import Error
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from dotenv import load_dotenv

load_dotenv()

# Função que se conecta ao banco MySQL e retorna a conexao
def conectar_banco():
    try:
        conexao = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),database=os.getenv("MYSQL_DATABASE"))
        return conexao   
    except Error as erro: 
        if erro.errno == 1049:
            print("Erro! O banco de dados informado não existe")
        elif erro.errno == 2005:
            print("Não foi possível encontrar o servidor MySQL")
        elif erro.errno == 1045:
            print("Falha de autenticação")
        else:
            print(erro)
        exit() 

# Função que se conecta ao MongoDB e retorna o DB segurança
def conectar_mongodb():
    try:
        client = MongoClient("mongodb://localhost:27017/",serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        db = client["segurança"]
        return db
    except ServerSelectionTimeoutError:
        print("Não foi possível se conectar ao MongoDB!")
        exit()