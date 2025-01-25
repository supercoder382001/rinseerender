from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import StreamingResponse
from supabase import create_client, Client
import asyncio
import json
import os
import base64

# app = FastAPI()
router = APIRouter()

url: str = "https://zmvjylvafmgqpxqtrblc.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inptdmp5bHZhZm1ncXB4cXRyYmxjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjM0ODk4MTIsImV4cCI6MjAzOTA2NTgxMn0.-qK5cu9zPoVtcpGAf14-XuJ55SMYXpfpXXgp6lz-Z4M"
supabase: Client = create_client(url, key)

response_success = {
    "response": True,
    "status": 1
}
response_failed = {
    "response": True,
    "status": 0
}
response_pending = {
    "response": False,
    "status": 2

}


async def event_stream(order_id: int):
    while True:
        # Query the latest payment status for the user
        response = supabase.table("phonepe").select("*").eq('merchantTransactionId', order_id).limit(1).execute()
        print(response)
        if response.data:
            decoded_bytes = base64.b64decode(response.data[0].get("response"))
            json_response = decoded_bytes.decode('utf-8')
            json_data = json.loads(json_response)
        if response.data and json_data["data"]["state"] == "COMPLETED":
            yield f"data: {json.dumps(response_success)}\n\n"
            break
            await asyncio.sleep(10)
        elif response.data and json_data["data"]["state"] == "FAILED":
            yield f"data: {json.dumps(response_failed)}\n\n"
            break
            await asyncio.sleep(10)
        else:
            yield f"data: {json.dumps(response_pending)}\n\n"
            await asyncio.sleep(5)  # Stream updates every 5 seconds


@router.post("/checkPayment")
async def checkPayment(order_id: int):
    return StreamingResponse(event_stream(order_id), media_type="text/event-stream")
