"""
Exemplos avançados de uso do DBConnector
"""
from dbconnector import connect, MySQLConnector
from dbconnector.utils import ConnectionPool
import threading

# 1. Uso com connection pool
print("=== Exemplo com Connection Pool ===")
pool = ConnectionPool(
    MySQLConnector,
    max_connections=3,
    host='localhost',
    user='root',
    password='senha',
    database='teste'
)

def worker(worker_id):
    """Simula trabalho concorrente com conexões do pool"""
    conn = pool.get_connection()
    try:
        cursor = conn.connection.cursor()
        cursor.execute("SELECT CONNECTION_ID()")
        conn_id = cursor.fetchone()[0]
        print(f"Worker {worker_id} usando conexão MySQL ID: {conn_id}")
    finally:
        pool.release_connection(conn)

# Simula 5 threads acessando o banco
threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

pool.close_all()

# 2. Transações e tratamento de erros
print("\n=== Exemplo com Transações ===")
try:
    with connect('sqlite', database='advanced.db') as conn:
        cursor = conn.connection.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY,
                owner TEXT,
                balance REAL
            )
        """)
        
        cursor.execute("DELETE FROM accounts")  # Limpa a tabela para o exemplo
        cursor.execute("INSERT INTO accounts (owner, balance) VALUES (?, ?)", 
                      ("Alice", 1000.0))
        cursor.execute("INSERT INTO accounts (owner, balance) VALUES (?, ?)", 
                      ("Bob", 500.0))
        
        # Transação de transferência
        try:
            # Debita da conta de Alice
            cursor.execute("UPDATE accounts SET balance = balance - ? WHERE owner = ?", 
                          (200.0, "Alice"))
            
            # Credita na conta de Bob
            cursor.execute("UPDATE accounts SET balance = balance + ? WHERE owner = ?", 
                          (200.0, "Bob"))
            
            conn.connection.commit()
            print("Transferência realizada com sucesso!")
        except Exception as e:
            conn.connection.rollback()
            print(f"Erro na transferência. Rollback realizado. Erro: {e}")
        
        # Verifica saldos
        cursor.execute("SELECT owner, balance FROM accounts")
        print("Saldos finais:", cursor.fetchall())
        
except Exception as e:
    print(f"Erro: {e}")