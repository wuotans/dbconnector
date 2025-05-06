from .connectors import (
    # Conectores SQL
    connect,
    MySQLConnector,
    PostgreSQLConnector,
    SQLiteConnector,
    OracleConnector,
    MSSQLConnector,
    
    # Conectores NoSQL
    MongoDBConnector,
    RedisConnector,
    CassandraConnector,
    ElasticsearchConnector,
    
    # Conectores Assíncronos
    AsyncMySQLConnector,
    AsyncPostgreSQLConnector,
    AsyncRedisConnector,
    AsyncElasticsearchConnector,
    
    # ORM e Utilitários
    SQLModel,
    DatabaseModel,
    ConnectionPool,
    
    # Exceções
    DatabaseConnectionError
)

__all__ = [
    # Função principal
    'connect',
    
    # SQL
    'MySQLConnector',
    'PostgreSQLConnector',
    'SQLiteConnector',
    'OracleConnector',
    'MSSQLConnector',
    
    # NoSQL
    'MongoDBConnector',
    'RedisConnector',
    'CassandraConnector',
    'ElasticsearchConnector',
    
    # Assíncrono
    'AsyncMySQLConnector',
    'AsyncPostgreSQLConnector',
    'AsyncRedisConnector',
    'AsyncElasticsearchConnector',
    
    # ORM
    'SQLModel',
    'DatabaseModel',
    
    # Utilitários
    'ConnectionPool',
    
    # Exceções
    'DatabaseConnectionError'
]

__version__ = '0.1.0'  # Atualize a versão conforme necessário