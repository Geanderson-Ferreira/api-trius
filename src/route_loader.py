import os
import importlib

def load_routes(app, prefix='api'):
    # Caminho para a pasta routes
    routes_dir = 'routes'

    # Itera sobre todas as pastas dentro de routes
    for version in os.listdir(routes_dir):
        version_path = os.path.join(routes_dir, version)
        
        if os.path.isdir(version_path):  # Verifica se é um diretório
            # Itera sobre todos os arquivos na pasta da versão
            for filename in os.listdir(version_path):
                if filename.endswith('.py') and filename != '__init__.py':
                    module_name = f'routes.{version}.{filename[:-3]}'
                    module = importlib.import_module(module_name)
                    
                    # Assume que cada módulo tem um objeto `router`
                    if hasattr(module, 'router'):
                        app.include_router(module.router, prefix=f"/{prefix}i/{version}")