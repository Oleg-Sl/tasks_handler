from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import all_routers


def get_application() -> FastAPI:
    application = FastAPI(
        title="PROJECT_NAME",
        debug=True,
        version="1.0.0",
        root_path="/task_handler",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return application


app = get_application()


for router in all_routers:
    app.include_router(router)
