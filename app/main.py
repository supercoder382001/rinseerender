from fastapi import FastAPI
from app.routers import mail, map, payment,phonepe
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
# Include routers
app.include_router(mail.router, prefix="/api", tags=["Mail"])
app.include_router(map.router, prefix="/api", tags=["Map"])
app.include_router(payment.router, prefix="/api", tags=["Payment"])
app.include_router(phonepe.router, prefix="/api", tags=["Phonepe"])
app.include_router(phonepepy.router, prefix="/api", tags=["Phonepepayment"])

@app.get("/")
async def root():
    return {"message": "Welcome to the combined FastAPI app"}
