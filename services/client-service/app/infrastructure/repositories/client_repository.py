from domain.repositories.client_repository_interface import ClientRepositoryInterface
from domain.entities.client import Client
from datetime import datetime
from infrastructure.logger.logger import get_logger

logger = get_logger("ClientRepository")

class ClientRepository(ClientRepositoryInterface):
    
    def save(self, client: Client, conn):
        cursor = conn.cursor()
        try:
            logger.info(f"Inserindo cliente no banco: {client.email}")

            cursor.execute("""
            INSERT INTO client (
                id, name, surname, email, birthdate,
                active, created_at, updated_at
            ) VALUES (
                :id, :name, :surname, :email, :birthdate,
                :active, :created_at, :updated_at
            )
        """, {
            "id": client.id,
            "name": client.name,
            "surname": client.surname,
            "email": client.email,
            "birthdate": client.birthdate,
            "active": 1 if client.active else 0,
            "created_at": client.created_at,
            "updated_at": client.updated_at
        })
            logger.info(f"Cliente inserido com sucesso: {client.id}, {client.created_at}")
        
        except Exception as e :
            logger.error(f"Erro ao inserir cliente : {client.id}, {str(e)}")
            raise
        finally:
            cursor.close()
    
    def get_by_id(self, client_id:str,conn):
        cursor = conn.cursor()
        try:
            logger.info(f"Executando SELECT por ID: {client_id}")
            cursor.execute("""
                SELECT id, name, surname, email, birthdate, active
                   created_at, updated_at
                FROM client
                WHERE id = :id
            """, {"id":client_id})
            
            row = cursor.fetchone()
        
            if not row:
                logger.warning(f"Nenhum cliente encontrado no banco: {client_id}")
                return None
            logger.info(f"Cliente retornado do banco: {client_id}")
            return self._map_to_entity(row)
    
        except Exception as e:
            logger.error(f" Erro ao SELECT ID : {str(e)}")
            raise
        finally:
            cursor.close()
        
         
    
    def get_all(self, conn):
        cursor = conn.cursor()
        try:
            logger.info("Executando SELECT de todos os clientes")
            
            cursor.execute("""
                SELECT id, name, surname, email, birthdate, active, created_at, updated_at
                FROM client
            """)
            rows = cursor.fetchall()
            
            logger.info(f"Total de clientes encontrados:{len(rows)}")
            return [self._map_to_entity(row) for row in rows]

            return rows
        except Exception as e:
            logger.error(f"Erro ao buscar todos os clientes: {str(e)}")
            raise
        finally:
            cursor.close()
        
    
    def get_all_active(self, conn):
        cursor = conn.cursor()
        try:
            logger.info(f"Executando SELECT de clientes ATIVOS.")
            cursor.execute("""
                SELECT id , name, surname, email, birthdate, active, created_at, updated_at
                FROM client
                WHERE active = 1
            """)
            rows = cursor.fetchall()
            logger.info(f"Clientes ativos encontrados: {len(rows)}")
            return [self._map_to_entity(row) for row in rows]
            
        except Exception as e:
            logger.error(f"Erro ao buscar clientes ativos: {str(e)}")
            raise
        finally:
            cursor.close()
            
    
    def get_all_inactive(self, conn):
        cursor = conn.cursor()
        try:
            logger.info(f"Executando SELECT para clientes inativados .")
            cursor.execute("""
                SELECT id, name, surname, email, birthdate, active, created_at, updated_at
                FROM client
                WHERE active = 0      
                       
            """)
            rows= cursor.fetchall()
            logger.info(f"Clientes inativos encontrados. {len(rows)}")
            return [self._map_to_entity(row) for row in rows]
        
        except Exception as e:
            logger.error(F"Erro ao encontrar clientes inativos{str(e)}")
            raise
        finally:
            cursor.close()
          
        
        
        
    def update(self, client: Client, conn):
        cursor = conn.cursor()
        try:
            logger.info(f"Atualizando cliente no banco:{client.id}")
        
            cursor.execute("""
                UPDATE client
                SET name = :name,
                    surname = :surname,
                    email = :email,
                    updated_at = :updated_at
                WHERE id = :id
            """, {
                "id": client.id,
                "name":client.name,
                "surname":client.surname,
                "email":client.email,
                
                "updated_at": datetime.now()
                })
            logger.info(f"Linhas afetadas: {cursor.rowcount}")
            
        except Exception as e:
            logger.error(f"Erro no Update: {str(e)}")
            raise
        finally:
            cursor.close()
        
    
    def delete(self, client_id: str, conn):
        cursor = conn.cursor()
        try:
            logger.info(f"Desativando cliente no banco: {client_id}")
            
            cursor.execute("""
                UPDATE client
                SET active = 0,
                    updated_at = :updated_at
                WHERE id = :id              
        """, {
            "id":client_id,
            "updated_at": datetime.now()
        })
            logger.info(f"Cliente desativado no banco. {client_id}")
        except Exception as e:
            logger.error(f"Erro no desativação: {str(e)}")
            raise
        finally:
            cursor.close()
    
            
    def _map_to_entity(self, row):
        client = Client(
            name=row[1],
            surname=row[2],
            email=row[3],
            birthdate=row[4]
        )
        client.id=row[0]
        client.active= bool(row[5])
        client.created_at = row[6]
        client.updated_at = row[7]
        
        return client   
    