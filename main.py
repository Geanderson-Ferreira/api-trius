from fastapi import FastAPI
from src.route_loader import load_routes

app = FastAPI(title="Integra Hotel", description="Integrador padrão de PMS")

# Carrega as rotas
load_routes(app, prefix='api')

# Roda a aplicação
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)