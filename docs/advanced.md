# Uso Avançado do DBConnector

## Connection Pooling

```python
from dbconnector.utils import ConnectionPool
from dbconnector import MySQLConnector

pool = ConnectionPool(
    MySQLConnector,
    max_connections=5,
    host='localhost',
    user='root',
    password='senha'
)

# Em aplicações web (exemplo com Flask)
@app.before_request
def get_db():
    if 'db_conn' not in g:
        g.db_conn = pool.get_connection()

@app.teardown_request
def close_db(exception):
    if 'db_conn' in g:
        pool.release_connection(g.db_conn)
```

## Operações com NoSQL

### Cassandra
```python
from dbconnector import connect

with connect('cassandra', hosts=['127.0.0.1']) as conn:
    conn.connection.execute(
        "INSERT INTO keyspace.table (id, name) VALUES (%s, %s)",
        (1, 'João')
    )
    
    rows = conn.connection.execute("SELECT * FROM keyspace.table")
    for row in rows:
        print(row)
```

### Elasticsearch (Assíncrono)
```python
import asyncio
from dbconnector import connect

async def search_products():
    async with connect('elasticsearch', async_conn=True) as conn:
        response = await conn.connection.search(
            index="products",
            body={"query": {"match_all": {}}}
        )
        print(response['hits']['hits'])

asyncio.run(search_products())
```

## ORM Avançado

```python
from dbconnector import SQLModel, connect

class Product(SQLModel):
    __tablename__ = 'products'
    __fields__ = {
        'id': 'SERIAL PRIMARY KEY',
        'name': 'TEXT NOT NULL',
        'price': 'DECIMAL(10,2)',
        'stock': 'INTEGER DEFAULT 0'
    }
    
    @classmethod
    def find_by_price_range(cls, connector, min_price, max_price):
        cursor = connector.connection.cursor()
        cursor.execute(
            f"SELECT * FROM {cls.get_table_name()} WHERE price BETWEEN %s AND %s",
            (min_price, max_price)
        )
        return [cls.from_dict(dict(row)) for row in cursor.fetchall()]

with connect('postgresql', database='ecommerce') as conn:
    Product.create_table(conn)
    
    # Insere produtos
    Product.insert(conn, {'name': 'Notebook', 'price': 4500.00})
    Product.insert(conn, {'name': 'Smartphone', 'price': 2500.00})
    
    # Consulta personalizada
    affordable = Product.find_by_price_range(conn, 2000.00, 3000.00)
    print("Produtos acessíveis:", [p.name for p in affordable])
```

## Migrações Básicas

```python
from dbconnector import connect

def migrate_v1_to_v2(connector):
    cursor = connector.connection.cursor()
    try:
        cursor.execute("ALTER TABLE products ADD COLUMN description TEXT")
        connector.connection.commit()
        print("Migração realizada com sucesso!")
    except Exception as e:
        connector.connection.rollback()
        print(f"Erro na migração: {e}")

with connect('sqlite', database='app.db') as conn:
    migrate_v1_to_v2(conn)
```

## Type Hints e Autocompletion

O pacote está totalmente tipado para melhor suporte em IDEs:

```python
def get_user(connector: BaseConnector, user_id: int) -> Optional[Dict[str, Any]]:
    """
    Obtém um usuário pelo ID
    
    Args:
        connector: Conector do banco de dados
        user_id: ID do usuário
    
    Returns:
        Dicionário com os dados do usuário ou None se não encontrado
    """
    if not isinstance(connector, BaseConnector):
        raise TypeError("connector must be a BaseConnector instance")
    
    cursor = connector.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    return dict(result) if result else None