from fastapi import FastAPI
from config import PROJECT_NAME, PROJECT_VERSION, ENVIRONMENT
from App.Routes.health import router as health_router
from App.Routes.V1.router import router as v1_router
from App.Database.database import Base, engine
from App.Models.chemical import ChemicalModel
from App.Models.ghs import GHSClassificationModel

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title=PROJECT_NAME,
    description="AI-Assisted Regulatory SDS & GHS Labeling Compliance Platform",
    version=PROJECT_VERSION,
)


@app.get("/")
def root():
    return {
        "message": "SDS-GHS Compliance Platform API is running",
        "version": PROJECT_VERSION,
        "environment": ENVIRONMENT,
    }


app.include_router(health_router)
app.include_router(v1_router)