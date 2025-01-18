from fastapi import FastAPI,APIRouter
from pydantic import BaseModel
from typing import Optional
import requests
import uuid
from app.models import total

# Create a FastAPI instance
# app = FastAPI()
router = APIRouter()


def geocode(name):
    external_api_url = "https://api.olamaps.io/places/v1/geocode"
    # access_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJMRndtX0U2akoyWG5yYkpkS1d1VXl2UllUN25lZ0FibDhWLXVSTno3UzZVIn0.eyJleHAiOjE3MzcxNjU1NDEsImlhdCI6MTczNzE2MTk0MSwianRpIjoiNjhjY2FhOTItZDA3Mi00MmFjLTkxMjEtMGYyZDI4MTk5OTYzIiwiaXNzIjoiaHR0cHM6Ly9hY2NvdW50Lm9sYW1hcHMuaW8vcmVhbG1zL29sYW1hcHMiLCJzdWIiOiJkMWM5NzU0MC1iNmE3LTQ2MWUtOGFiMC0xZjQxZmM2NDFhNWMiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiI5OGM2ZWVjNy1iMWM5LTQ2NGItYWY2ZS01NTU0YjBjYWU1ZjIiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIlNCTi1hNTI0OTZiYy0wYzcxLTQxZjYtYjM3Ny05YTRkZmM5ZTBlMzEiLCJPUkctNzMzNDQ3NTUtNjU2Zi00YjUzLWE1ZDItMjIwZjEzNzc3ZjM2IiwiZGVmYXVsdC1yb2xlcy1vbGFtYXBzIl19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJjbGllbnRIb3N0IjpudWxsLCJvcmciOiJPUkctNzMzNDQ3NTUtNjU2Zi00YjUzLWE1ZDItMjIwZjEzNzc3ZjM2Iiwib3JnMSI6e30sInJlYWxtIjoib2xhbWFwcyIsInByZWZlcnJlZF91c2VybmFtZSI6InNlcnZpY2UtYWNjb3VudC05OGM2ZWVjNy1iMWM5LTQ2NGItYWY2ZS01NTU0YjBjYWU1ZjIiLCJjbGllbnRBZGRyZXNzIjpudWxsLCJjbGllbnRfaWQiOiI5OGM2ZWVjNy1iMWM5LTQ2NGItYWY2ZS01NTU0YjBjYWU1ZjIiLCJzYm4iOiJTQk4tYTUyNDk2YmMtMGM3MS00MWY2LWIzNzctOWE0ZGZjOWUwZTMxIn0.pssCV0RiFqj6UT1wVI2_AN8Mq2vAOelH6P7wIIVlvzkfJLgNeZz22EHKW0imflxC2bTgHFJ97NdRA6C5w54A_uEG7JDXGsSNaGV-D7aydeJH_buhynRwQvaNwq2U7dzWdx03WPUzqULLohLUabY2j0Jgk7xRkMEd9juZZkBEIjtEcjtQF5YXXuhRNsp4v3LQFloVm78Us2PoXA-qE7FifEEi6bbdGIfX0JHOQ0JwUDUghX_7Y-AU-vLK41yJ_MoEXhNgsMaDNaFXMFYuv0nVizENTnOV9x_5Zp4PFMFzI5OwInLts7vhBOTmkBxYkuZgbzZt25C22Zw_C0Evbf5Yaw"  # Replace with your token

    headers = {
        # "Authorization": f"Bearer {access_token}",
        "accept": "application/json",
        "X-Request-Id": str(uuid.uuid4()),
        "X-Correlation-Id": str(uuid.uuid4())
    }
    params = {"address": name, "language": "English", "api_key": "kVbhvshzybFfK6kCH8S3TrhJX71g2W1QKDPKcGhx"}

    response = requests.get(external_api_url, headers=headers, params=params)
    if response.status_code == 200:
        try:
            response_data = response.json()
            geocoding_results = response_data.get("geocodingResults", [])

            extracted_results = []
            for result in geocoding_results:
                address_components = result.get("address_components", [])
                geometry = result.get("geometry", {}).get("location", {})

                postal_code = next(
                    (comp["long_name"] for comp in address_components if "postal_code" in comp["types"]), None)
                city = next(
                    (comp["long_name"] for comp in address_components if "locality" in comp["types"]), None)
                state = next(
                    (comp["long_name"] for comp in address_components if
                     "administrative_area_level_1" in comp["types"]), None)

                formatted_address = result.get("formatted_address", "")
                latitude = geometry.get("lat", None)
                longitude = geometry.get("lng", None)

                extracted_results.append({
                    "postal_code": postal_code,
                    "city": city,
                    "state": state,
                    "formatted_address": formatted_address,
                    "latitude": latitude,
                    "longitude": longitude
                })

            return {
                "message": "Successfully fetched and processed data from external API",
                "formatted_results": extracted_results
            }
        except KeyError as e:
            return {
                "message": "Error processing the response data",
                "error": str(e)
            }
    else:
        return {
            "message": "Failed to fetch data from external API",
            "status_code": response.status_code,
            "error": response.text
        }


def reversegeocode(latitude, longitude):
    external_api_url = "https://api.olamaps.io/places/v1/reverse-geocode"
    # access_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJMRndtX0U2akoyWG5yYkpkS1d1VXl2UllUN25lZ0FibDhWLXVSTno3UzZVIn0.eyJleHAiOjE3MzcxNjU1NDEsImlhdCI6MTczNzE2MTk0MSwianRpIjoiNjhjY2FhOTItZDA3Mi00MmFjLTkxMjEtMGYyZDI4MTk5OTYzIiwiaXNzIjoiaHR0cHM6Ly9hY2NvdW50Lm9sYW1hcHMuaW8vcmVhbG1zL29sYW1hcHMiLCJzdWIiOiJkMWM5NzU0MC1iNmE3LTQ2MWUtOGFiMC0xZjQxZmM2NDFhNWMiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiI5OGM2ZWVjNy1iMWM5LTQ2NGItYWY2ZS01NTU0YjBjYWU1ZjIiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIlNCTi1hNTI0OTZiYy0wYzcxLTQxZjYtYjM3Ny05YTRkZmM5ZTBlMzEiLCJPUkctNzMzNDQ3NTUtNjU2Zi00YjUzLWE1ZDItMjIwZjEzNzc3ZjM2IiwiZGVmYXVsdC1yb2xlcy1vbGFtYXBzIl19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJjbGllbnRIb3N0IjpudWxsLCJvcmciOiJPUkctNzMzNDQ3NTUtNjU2Zi00YjUzLWE1ZDItMjIwZjEzNzc3ZjM2Iiwib3JnMSI6e30sInJlYWxtIjoib2xhbWFwcyIsInByZWZlcnJlZF91c2VybmFtZSI6InNlcnZpY2UtYWNjb3VudC05OGM2ZWVjNy1iMWM5LTQ2NGItYWY2ZS01NTU0YjBjYWU1ZjIiLCJjbGllbnRBZGRyZXNzIjpudWxsLCJjbGllbnRfaWQiOiI5OGM2ZWVjNy1iMWM5LTQ2NGItYWY2ZS01NTU0YjBjYWU1ZjIiLCJzYm4iOiJTQk4tYTUyNDk2YmMtMGM3MS00MWY2LWIzNzctOWE0ZGZjOWUwZTMxIn0.pssCV0RiFqj6UT1wVI2_AN8Mq2vAOelH6P7wIIVlvzkfJLgNeZz22EHKW0imflxC2bTgHFJ97NdRA6C5w54A_uEG7JDXGsSNaGV-D7aydeJH_buhynRwQvaNwq2U7dzWdx03WPUzqULLohLUabY2j0Jgk7xRkMEd9juZZkBEIjtEcjtQF5YXXuhRNsp4v3LQFloVm78Us2PoXA-qE7FifEEi6bbdGIfX0JHOQ0JwUDUghX_7Y-AU-vLK41yJ_MoEXhNgsMaDNaFXMFYuv0nVizENTnOV9x_5Zp4PFMFzI5OwInLts7vhBOTmkBxYkuZgbzZt25C22Zw_C0Evbf5Yaw"  # Replace with your token

    headers = {
        # "Authorization": f"Bearer {access_token}",
        "accept": "application/json",
        "X-Request-Id": str(uuid.uuid4()),
        "X-Correlation-Id": str(uuid.uuid4())
    }
    params = {"latlng": f"{latitude},{longitude}", "api_key": "kVbhvshzybFfK6kCH8S3TrhJX71g2W1QKDPKcGhx"}

    response = requests.get(external_api_url, headers=headers, params=params)
    if response.status_code == 200:
        try:
            response_data = response.json()
            results = response_data.get("results", [])

            extracted_results = []
            for result in results:
                address_components = result.get("address_components", [])
                geometry = result.get("geometry", {}).get("location", {})

                postal_code = next(
                    (comp["long_name"] for comp in address_components if "postal_code" in comp["types"]), None)
                city = next(
                    (comp["long_name"] for comp in address_components if "locality" in comp["types"]), None)
                state = next(
                    (comp["long_name"] for comp in address_components if
                     "administrative_area_level_1" in comp["types"]), None)

                formatted_address = result.get("formatted_address", "")
                latitude = geometry.get("lat", None)
                longitude = geometry.get("lng", None)

                extracted_results.append({
                    "postal_code": postal_code,
                    "city": city,
                    "state": state,
                    "formatted_address": formatted_address,
                    "latitude": latitude,
                    "longitude": longitude
                })

            return {
                "message": "Successfully fetched and processed data from external API",
                "formatted_results": extracted_results
            }
        except KeyError as e:
            return {
                "message": "Error processing the response data",
                "error": str(e)
            }
    else:
        return {
            "message": "Failed to fetch data from external API",
            "status_code": response.status_code,
            "error": response.text
        }


# Define a GET endpoint with query parameters
@router.post("/map/")
async def maps(item: total):
    if item.method == 1:
        message = reversegeocode(item.latitude, item.longitude)
        return message
    if item.method == 2:
        message = geocode(item.name)
        return message
