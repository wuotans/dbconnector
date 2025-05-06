# DBConnector - Exemplos Completos

## 1. Aplicação Web com Connection Pool

```python
from flask import Flask, g
from dbconnector.utils import ConnectionPool
from dbconnector import PostgreSQLConnector

app = Flask(__name__)
pool = ConnectionPool(
    PostgreSQLConnector,
    max_connections=5,
    host='localhost',
    user='webuser',
    password='webpass',
    database='webdb'
)

@app.before_request
def get_db():
    g.db = pool.get_connection()

@app.route('/users')
def list_users():
    cursor = g.db.connection.cursor()
    cursor.execute("SELECT * FROM users")
    return {'users': cursor.fetchall()}

@app.teardown_request
def close_db(exception):
    if 'db' in g:
        pool.release_connection(g.db)
```

## 2. Migração de Dados entre Bancos

```python
from dbconnector import connect

def migrate_mysql_to_postgresql():
    with connect('mysql', host='old-server', user='admin', password='admin') as src, \
         connect('postgresql', host='new-server', user='admin', password='admin') as dest:
        
        # Ler dados do MySQL
        src_cursor = src.connection.cursor(dictionary=True)
        src_cursor.execute("SELECT * FROM products")
        products = src_cursor.fetchall()
        
        # Escrever no PostgreSQL
        dest_cursor = dest.connection.cursor()
        for product in products:
            dest_cursor.execute(
                "INSERT INTO products (id, name, price) VALUES (%s, %s, %s)",
                (product['id'], product['name'], product['price'])
            )
        dest.connection.commit()
```

## 3. Sistema de Cache com Redis

```python
from dbconnector import connect
import time

def get_expensive_data(key):
    # Tenta obter do cache primeiro
    with connect('redis', host='cache-server') as cache:
        data = cache.connection.get(key)
        if data:
            return data
    
    # Se não existir no cache, calcula e armazena
    data = calculate_expensive_data(key)
    
    with connect('redis', host='cache-server') as cache:
        cache.connection.setex(key, 3600, data)  # Expira em 1 hora
    
    return data
```

## 4. Análise de Dados com Pandas

```python
from dbconnector import connect
import pandas as pd

with connect('postgresql', host='data-warehouse') as conn:
    # Ler dados diretamente para um DataFrame
    df = pd.read_sql("SELECT * FROM sales WHERE date > '2023-01-01'", conn.connection)
    
    # Análise
    monthly_sales = df.groupby(pd.to_datetime(df['date']).dt.month)['amount'].sum()
    print(monthly_sales.plot(kind='bar'))
```

## 5. Aplicação Assíncrona

```python
import asyncio
from dbconnector import connect

async def process_user(user_id):
    async with connect('postgresql', async_conn=True, 
                      host='localhost', user='async_user') as conn:
        # Consulta assíncrona
        rows = await conn.connection.fetch(
            "SELECT * FROM user_activity WHERE user_id = $1", 
            user_id
        )
        return rows

async def main():
    tasks = [process_user(i) for i in range(1, 101)]
    results = await asyncio.gather(*tasks)
    print(f"Processed {len(results)} users")

asyncio.run(main())
```