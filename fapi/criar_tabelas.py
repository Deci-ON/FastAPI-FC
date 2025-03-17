from core.configs import settings
from core.database import engines  # Aqui importamos os engines
import logging

# Configuração do logging
logging.basicConfig(
    filename="barramento_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def create_tables() -> None:
    import models.__all_models  # Certifique-se de que este caminho está correto

    # Usar o engine específico para o barramento
    engine_barramento = engines["BARRA"]

    logging.info("Iniciando criação de tabelas no barramento")
    print("Criando as tabelas no barramento...")
    print(f"Conectado ao banco de dados: {engine_barramento.url}")

    try:
        # Criar as tabelas no banco BARRA
        with engine_barramento.connect() as conn:
            # Dropar e criar as tabelas
            settings.DBBaseModel.metadata.drop_all(bind=conn)
            settings.DBBaseModel.metadata.create_all(bind=conn)
            conn.commit()  # Confirma a transação

        logging.info("Tabelas criadas com sucesso no barramento")
        print("Tabelas criadas com sucesso no barramento")

    except Exception as e:
        erro_msg = f"Erro ao criar tabelas no barramento: {str(e)}"
        logging.error(erro_msg)
        print(erro_msg)

    finally:
        # Fecha a conexão corretamente
        engine_barramento.dispose()
        logging.info("Conexão com o barramento fechada.")

def main():
    create_tables()

if __name__ == '__main__':
    main()
