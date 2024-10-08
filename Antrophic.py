from fastapi import FastAPI, HTTPException
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import logging
import json


# Configurar el nivel de logging
logging.basicConfig(level=logging.INFO)

# Inicia FastAPI
app = FastAPI()

# Cargar variables de entorno (como la API key)
load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')

# Configuración del modelo Anthropic a través de LangChain
llm = ChatAnthropic(anthropic_api_key=api_key, model="claude-3-sonnet-20240229", temperature=0.2)

# Esquema JSON para estructurar la salida
# Esquema JSON para estructurar la salida
# Esquema JSON para estructurar la salida
vehicle_json_schema = {
    "title": "vehicle_specifications",
    "description": "Technical specifications of a vehicle.",
    "type": "object",
    "properties": {
        "brand": {
            "type": "string",
            "description": "The brand of the vehicle.",
        },
        "model": {
            "type": "string",
            "description": "The model of the vehicle.",
        },
        "version": {
            "type": "string",
            "description": "The version or complete version of the vehicle (if applicable).",
            "default": None,
        },
        "year": {
            "type": "integer",
            "description": "The year of manufacturing of the vehicle.",
        },
        "body_type": {
            "type": "string",
            "description": "The type of the vehicle's body.",
            "enum": [
                "Turismo familiar",
                "Turismo",
                "Todoterreno",
                "Vehículo comercial",
                "Descapotable",
                "Pick Up",
                "Monovolumen",
                "Coupé",
                "Monovolumen_parecido_a_vehículo_comercial"
            ]
        },
        "doors": {
            "type": "integer",
            "description": "The number of doors the vehicle has.",
            "default": None,
        },
        "status": {
            "type": "string",
            "description": "The status of the vehicle (e.g., for sale, discontinued).",
            "default": None,
        },
        "length": {
            "type": "integer",
            "description": "The length of the vehicle in millimeters (mm).",
            "default": None,
        },
        "seats": {
            "type": "integer",
            "description": "The number of seats in the vehicle.",
            "default": None,
        },
        "price": {
            "type": "number",
            "description": "The price of the vehicle in euros (€).",
            "default": None,
        },
        "technology": {
            "type": "string",
            "description": "The technology of the vehicle.",
            "enum": [
                "HEV",
                "MHEV",
                "PHEV",
                "EV",
                "EREV",
                "Combustion"
            ]
        },
        "transmission": {
            "type": "string",
            "description": "The type of transmission (e.g., manual, automatic).",
            "default": None,
        },
        "fuel_consumption": {
            "type": "number",
            "description": "The combined fuel consumption in liters per 100 kilometers (l/100km).",
            "default": None,
        },
        "fuel_type": {
            "type": "string",
            "description": "The type of fuel the vehicle uses.",
            "enum": [
                "gasoleo",
                "gasolina",
                "electricidad",
                "etanol",
                "gas natural",
                "glp",
                "hidrogeno"
            ]
        },
        "electric_range": {
            "type": "integer",
            "description": "The electric range of the vehicle in kilometers (km), if applicable.",
            "default": None,
        },
        "battery_capacity": {
            "type": "number",
            "description": "The gross or net capacity of the battery in kilowatt-hours (kWh), if applicable.",
            "default": None,
        },
        "electric_consumption": {
            "type": "number",
            "description": "The combined electric consumption in kilowatt-hours per 100 kilometers (kWh/100km), if applicable.",
            "default": None,
        },
        "charging_time": {
            "type": "number",
            "description": "The charging time in alternating current (AC) in hours (h), if applicable.",
            "default": None,
        },
        "duplicate_date": {
            "type": "string",
            "description": "A date to distinguish between duplicates in the format MMM-YY (e.g., Sep-24).",
        },
        "max_power": {
            "type": "object",
            "properties": {
                "cv": {
                    "type": "integer",
                    "description": "Horsepower of the vehicle.",
                    "default": None,
                },
                "kw": {
                    "type": "integer",
                    "description": "Kilowatts of the vehicle.",
                    "default": None,
                }
            },
            "default": None,
        },
        "acceleration": {
            "type": "number",
            "description": "The time it takes to accelerate from 0 to 100 km/h in seconds.",
            "default": None,
        },
        "displacement": {
            "type": "integer",
            "description": "The engine displacement in cubic centimeters (cc).",
            "default": None,
        },
        "environmental_label": {
            "type": "string",
            "description": "The vehicle's environmental label (e.g., Euro 6).",
            "default": None,
        },
        "co2_emissions": {
            "type": "number",
            "description": "The CO2 emissions in grams per kilometer (gCO2/km).",
            "default": None,
        },
        "tank_capacity": {
            "type": "number",
            "description": "The fuel tank capacity in liters (l) or kilograms (kg), depending on fuel type.",
            "default": None,
        },
        "max_speed": {
            "type": "number",
            "description": "The maximum speed of the vehicle in kilometers per hour (km/h).",
            "default": None,
        },
        "maintenance_costs": {
            "type": "number",
            "description": "The monthly maintenance costs in euros per month (€/month).",
            "default": None,
        },
        "euro_ncap_rating": {
            "type": "integer",
            "description": "The EuroNCAP rating in stars.",
            "default": None,
        },
        "sources": {
            "type": "string",
            "description": "List of web pages from which data were extracted",
            "default": None,
        }
    }
}




# Crear un LLM con salida estructurada
structured_llm = llm.with_structured_output(vehicle_json_schema)

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
        # Prompt template para LangChain
        prompt = f"""
                    You are an assistant that extracts technical specifications for vehicles based on the following schema. 
                    Your response **MUST** be in valid JSON format, and it **MUST** match the provided schema exactly, without adding any additional fields or nesting.
                    Do not include any additional properties or explanations.

                    Schema:
                    {json.dumps(vehicle_json_schema, indent=2)}

                    Extract the specifications from the following description:
                    {request.description}

                    You must look for all the data missing in the description in websites. If you can´t find a field set it to null.
                    Return **ONLY** the JSON data, strictly following the schema above.
                    """

        # Invocar el modelo con el prompt y obtener el JSON estructurado
        vehicle_data = structured_llm.invoke(prompt)

        # Imprimir el contenido JSON en consola
        print(vehicle_data)



        return {"vehicle_data": vehicle_data}

    except Exception as e:
        logging.error(f"Error inesperado: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
