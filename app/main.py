from fastapi import FastAPI
from app.routers import mail, map, payment,phonepe

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include routers
app.include_router(mail.router, prefix="/api", tags=["Mail"])
app.include_router(map.router, prefix="/api", tags=["Map"])
app.include_router(payment.router, prefix="/api", tags=["Payment"])
app.include_router(phonepe.router, prefix="/api", tags=["Phonepe"])

@app.get("/")
async def root():
    return {"message": "Welcome to the combined FastAPI app"}
