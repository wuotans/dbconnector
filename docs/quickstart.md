# DBConnector - Guia Rápido

## Instalação

```bash
# Instalação básica
pip install dbconnector

# Com suporte a MySQL e PostgreSQL
pip install dbconnector[sql]

# Com suporte a MongoDB
pip install dbconnector[mongodb]
```

## Conexão Básica

### SQL (MySQL, PostgreSQL, SQLite)

```python
from dbconnector import connect

# MySQL
with connect('mysql', 
             host='localhost',
             user='usuario',
             password='senha',
             database='meubanco') as conn:
    cursor = conn.connection.cursor()
    cursor.execute("SELECT * FROM usuarios")
    print(cursor.fetchall())

# SQLite (não requer servidor)
with connect('sqlite', database=':memory:') as conn:
    conn.connection.execute("CREATE TABLE teste (id INTEGER, nome TEXT)")
    conn.connection.execute("INSERT INTO teste VALUES (1, 'Exemplo')")
    print(conn.connection.execute("SELECT * FROM teste").fetchall())
```

### NoSQL (MongoDB, Redis)

```python
# MongoDB
with connect('mongodb', host='localhost', port=27017) as conn:
    db = conn.connection['meubanco']
    colecao = db['minhacolecao']
    colecao.insert_one({"nome": "João", "idade": 30})
    print(list(colecao.find()))

# Redis
with connect('redis', host='localhost') as conn:
    conn.connection.set('chave', 'valor')
    print(conn.connection.get('chave'))
```

## Operações CRUD Básicas

```python
# Inserir dados
with connect('sqlite', database='exemplo.db') as conn:
    cursor = conn.connection.cursor()
    cursor.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", 
                  ("Maria", "maria@exemplo.com"))
    conn.connection.commit()

# Consultar dados
with connect('sqlite', database='exemplo.db') as conn:
    cursor = conn.connection.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nome = ?", ("Maria",))
    print(cursor.fetchone())
```

## Próximos Passos

- [Guia Avançado](advanced.md) - Pool de conexões, ORM e operações assíncronas
- [Exemplos Completos](examples.md) - Casos de uso reais