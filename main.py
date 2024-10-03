from fastapi import FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import logging
import json


logging.basicConfig(level=logging.INFO)

# Inicia FastAPI
app = FastAPI()

load_dotenv()
api_key = os.getenv('API_KEY')
client = OpenAI(api_key=api_key)


# Modelo Pydantic para validar las solicitudes
class VehicleRequest(BaseModel):
    description: str  # Descripción del vehículo para extraer las especificaciones


@app.get("/")
async def root():
    return {"message": "End point raíz"}

# Endpoint para extraer las especificaciones del vehículo
@app.post("/extract-specifications/")
async def extract_vehicle_specifications(request: VehicleRequest):
    try:
        # El prompt que usaremos para hacer la solicitud a la API de OpenAI
        prompt = f"""
        You are an assistant that extracts technical specifications for vehicles. Given a car, extract and return the data in JSON format with the following fields:

        1. "brand" (string): The brand of the vehicle (e.g., "Toyota").
        2. "model" (string): The model of the vehicle (e.g., "Corolla").
        3. "version" (string): The version or complete version of the vehicle (if applicable).
        4. "year" (integer): The year of manufacturing of the vehicle.
        5. "body_type" (string): The type of the vehicle's body (e.g., "sedan", "SUV").
        6. "doors" (integer): The number of doors the vehicle has.
        7. "status" (string): Whether the vehicle is currently "for sale", "discontinued", or other relevant status.
        8. "length" (integer): The length of the vehicle in millimeters (mm).
        9. "seats" (integer): The number of seats in the vehicle.
        10. "price" (number): The price of the vehicle in euros (€).
        11. "technology" (string): The technology of the vehicle (e.g., "hybrid", "electric", "combustion").
        12. "transmission" (string): The type of transmission (e.g., "manual", "automatic").
        13. "fuel_consumption" (number): The combined fuel consumption in liters per 100 kilometers (l/100km).
        14. "fuel_type" (string): The type of fuel the vehicle uses (e.g., "gasoline", "diesel", "electric").
        15. "electric_range" (integer): The electric range of the vehicle in kilometers (km), if applicable.
        16. "battery_capacity" (number): The gross or net capacity of the battery in kilowatt-hours (kWh), if applicable.
        17. "electric_consumption" (number): The combined electric consumption in kilowatt-hours per 100 kilometers (kWh/100km), if applicable.
        18. "charging_time" (number): The charging time in alternating current (AC) in hours (h), if applicable.
        19. "duplicate_date" (string): A date that helps to distinguish between duplicates in the format "MMM-YY" (e.g., "Sep-24").
        20. "max_power" (object): The maximum power of the vehicle in horsepower (CV) and kilowatts (kW).
            - "cv" (integer): Horsepower of the vehicle.
            - "kw" (integer): Kilowatts of the vehicle.
        21. "acceleration" (number): The time it takes to accelerate from 0 to 100 km/h in seconds.
        22. "displacement" (integer): The engine displacement in cubic centimeters (cc).
        23. "environmental_label" (string): The vehicle's environmental label (e.g., "Euro 6").
        24. "co2_emissions" (number): The CO2 emissions in grams per kilometer (gCO2/km).
        25. "tank_capacity" (number): The fuel tank capacity in liters (l) or kilograms (kg), depending on fuel type.
        26. "max_speed" (number): The maximum speed of the vehicle in kilometers per hour (km/h).
        27. "maintenance_costs" (number): The monthly maintenance costs in euros per month (€/month).
        28. "euro_ncap_rating" (integer): The EuroNCAP rating in stars.
        
        Return the result in JSON format. If a value is not available, set it to `null`.
        
        I want you to look for car information on manufacturers' websites and specialized car websites, such as "coches.net". Also add a field indicating from where you have extracted the information.
        
        Here is the description of the vehicle: {request.description}
        
        SHOW ONLY THE JSON.
        """

        # Llamada a la API de OpenAI
        response = client.chat.completions.create(model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.3)

        vehicle_data = response.choices[0].message.content

        # Imprimir el contenido JSON en consola
        print(vehicle_data)  # Aquí se imprime el JSON recibido

        return {"message": "JSON printed in console!"}


    except json.JSONDecodeError as jde:

        print(f"Error al decodificar JSON: {str(jde)}")

        raise HTTPException(status_code=500, detail="Error al decodificar la respuesta de OpenAI en JSON.")

    except Exception as e:

        print(f"Error: {str(e)}")

        raise HTTPException(status_code=500, detail=str(e))
