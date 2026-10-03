from fastapi import FastAPI

app = FastAPI(
    title="SDS-GHS Compliance Platform",
    description="AI-Assisted Regulatory SDS & GHS Labeling Compliance Platform",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "SDS-GHS Compliance Platform API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }