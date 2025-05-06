# DBConnector

[![PyPI version](https://badge.fury.io/py/dbconnector.svg)](https://badge.fury.io/py/dbconnector)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/dbconnector.svg)](https://pypi.org/project/dbconnector/)

Um pacote Python completo para conexão com bancos de dados SQL e NoSQL, com suporte a operações assíncronas e ORM básico.

## Recursos

- Conexão simplificada com diversos bancos de dados
- Suporte a SQL (MySQL, PostgreSQL, SQLite, Oracle, MSSQL) e NoSQL (MongoDB, Redis, Cassandra, Elasticsearch)
- Operações assíncronas
- ORM básico para operações CRUD
- Pool de conexões
- CLI para testes rápidos
- Tipagem completa para melhor suporte a IDEs

## Instalação

Instalação básica:
```bash
pip install dbconnector
```

Instalação com suporte a bancos específicos:
```bash
pip install dbconnector[sql]          # Bancos SQL
pip install dbconnector[mongodb]      # MongoDB
pip install dbconnector[elasticsearch] # Elasticsearch
pip install dbconnector[async]        # Suporte assíncrono
pip install dbconnector[all]          # Todos os recursos
```

## Uso Básico

### Conexão Simples
```python
from dbconnector import connect

# SQL
with connect('mysql', host='localhost', user='root', password='senha') as conn:
    cursor = conn.connection.cursor()
    cursor.execute("SELECT 1")
    print(cursor.fetchone())

# NoSQL (MongoDB)
with connect('mongodb', host='localhost') as conn:
    db = conn.connection['meu_banco']
    print(db.list_collection_names())
```

### Operações Assíncronas
```python
import asyncio
from dbconnector import connect

async def test_async():
    async with connect('postgresql', async_conn=True, 
                      host='localhost', user='postgres') as conn:
        result = await conn.connection.fetch("SELECT 1")
        print(result)

asyncio.run(test_async())
```

### ORM Básico
```python
from dbconnector import SQLModel, connect

class User(SQLModel):
    __fields__ = {
        'id': 'INTEGER PRIMARY KEY',
        'name': 'TEXT NOT NULL',
        'email': 'TEXT UNIQUE'
    }

with connect('sqlite', database=':memory:') as conn:
    User.create_table(conn)
    
    user_id = User.insert(conn, {'name': 'João', 'email': 'joao@exemplo.com'})
    print(f"Usuário inserido com ID: {user_id}")
```

## CLI

O pacote inclui uma CLI para testes rápidos:

```bash
dbconnector-cli test --type mysql --host localhost --user root
```

Opções disponíveis:
- `--type`: Tipo de banco de dados (obrigatório)
- `--host`, `--port`, `--user`, `--password`, `--database`: Parâmetros de conexão
- `--async`: Usar conexão assíncrona

## Documentação Completa

Consulte a [documentação avançada](docs/advanced.md) para:
- Uso do connection pool
- Operações com NoSQL
- Transações
- Configuração de logging
- Decoradores úteis

## Contribuição

Contribuições são bem-vindas! Por favor, abra uma issue ou envie um pull request.