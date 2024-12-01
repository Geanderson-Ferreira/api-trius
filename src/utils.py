import datetime
import psycopg2
from os import environ
from dotenv import load_dotenv

load_dotenv()

class Logger:
    def __init__(self, filename='log.txt'):
        self.allowedLogs = ['TERMINAL', 'DB', 'TXT']
        self.LOGLEVEL = environ.get('LEVEL_LOG', '')
        self.filename = filename

    def _log(self, level, message):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        formatted_message = f'[{timestamp}] {level}: {message}'
        
        if self.LOGLEVEL == 'DB':
            self._log_to_db(level, message)
            return  # Evita continuar e cair no bloco else
        elif self.LOGLEVEL == 'TXT':
            self._log_to_txt(formatted_message)
            return
        elif self.LOGLEVEL == 'TERMINAL':
            self._log_to_terminal(formatted_message)
            return
        elif self.LOGLEVEL not in self.allowedLogs:
            # Somente imprime essa mensagem se o LEVEL_LOG for inválido ou não definido
            print('Variável de ambiente "LEVEL_LOG" não definida ou incorreta. Valores aceitos: "TXT", "DB", "TERMINAL".')
            print(formatted_message)

    def _log_to_db(self, level, message):
        if level != 'OUTER':#'INFO':  # Log no banco só para níveis acima de INFO
            try:
                connection = psycopg2.connect(
                    database=environ.get('DATA_BASE_NAME'),
                    user=environ.get('DATA_BASE_USER'),
                    host=environ.get('DATA_BASE_URL'),
                    password=environ.get('DATA_BASE_PASSWORD'),
                    port=environ.get('DATA_BASE_PORT')
                )
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO log (log_level, log_info)
                    VALUES (%s, %s);
                """, (level, message))
                
                connection.commit()
                cursor.close()
                connection.close()
            except Exception as e:
                print(f"Erro ao salvar log no banco de dados: {e}")

    def _log_to_txt(self, formatted_message):
        try:
            with open(self.filename, 'a') as logfile:
                logfile.write(formatted_message + '\n')
        except Exception as e:
            print(f"Erro ao salvar log no arquivo TXT: {e}")

    def _log_to_terminal(self, formatted_message):
        print(formatted_message)

    def error(self, message):
        self._log('ERROR', message)

    def warning(self, message):
        self._log('WARNING', message)

    def info(self, message):
        self._log('INFO', message)

    def success(self, message):
        self._log('SUCCESS', message)
