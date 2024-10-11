import os
import importlib

def load_routes(app, routes_dir='routes'):
    
    for filename in os.listdir(routes_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f'routes.{filename[:-3]}'  # Remove '.py' do nome do arquivo
            module = importlib.import_module(module_name)
            
            if hasattr(module, 'router'):
                app.include_router(module.router)