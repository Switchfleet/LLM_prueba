# Vehicle Specifications Extractor API

This is a FastAPI-based application that allows users to extract technical specifications for vehicles using the OpenAI GPT-4 API. Given a vehicle description, the API will return the relevant specifications in JSON format.

## Features

- Extracts vehicle specifications such as brand, model, year, engine type, max speed, fuel consumption, etc.
- Returns the specifications in a structured JSON format.
- If a value is unavailable, the API will set it to `null`.

## Requirements

- Python 3.12.2
- OpenAI API Key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/
   cd 
   
2. Install Poetry (if not already installed)

3. Install dependencies using Poetry:
   ```bash
   poetry install
 
## Running the API
```bash
   poetry run uvicorn main:app --reload
   ```
## Usage
Method: POST

Description: Extract vehicle specifications from a given vehicle description.

Request Body:

```bash
{
    "description": "Toyota Corolla 2023 Hybrid, 5-door, automatic transmission, Euro 6, max speed 180 km/h, price 25,000 euros."
}
```

