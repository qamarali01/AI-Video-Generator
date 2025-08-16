from app import app
from app.routes import router
from middleware import CORSMiddlewareWithOptions

app.add_middleware(CORSMiddlewareWithOptions)
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)