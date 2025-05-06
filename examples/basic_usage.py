"""
Exemplos básicos de uso do DBConnector
"""
from dbconnector import connect

# 1. Conexão com MySQL
print("=== Exemplo com MySQL ===")
try:
    with connect(
        'mysql',
        host='localhost',
        user='root',
        password='senha',
        database='teste'
    ) as conn:
        cursor = conn.connection.cursor()
        cursor.execute("SHOW TABLES")
        print("Tabelas no banco de dados:", cursor.fetchall())
except Exception as e:
    print(f"Erro ao conectar ao MySQL: {e}")

# 2. Conexão com SQLite
print("\n=== Exemplo com SQLite ===")
try:
    with connect('sqlite', database='example.db') as conn:
        cursor = conn.connection.cursor()
        
        # Cria uma tabela se não existir
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT
            )
        """)
        
        # Insere dados
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", 
                      ("João Silva", "joao@example.com"))
        
        # Consulta dados
        cursor.execute("SELECT * FROM users")
        print("Usuários:", cursor.fetchall())
        
        conn.connection.commit()
except Exception as e:
    print(f"Erro ao conectar ao SQLite: {e}")