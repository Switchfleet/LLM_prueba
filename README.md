# LLM POC

This is a FastAPI-based application that allows users to extract technical specifications for vehicles using the OpenAI GPT-4 API. Given a vehicle description, the API will return the relevant specifications in JSON format.

## Features

- Extracts vehicle specifications such as brand, model, year, engine type, max speed, fuel consumption, etc.
- Returns the specifications in a structured JSON format.
- If a value is unavailable, the API will set it to `null`.

## Requirements

- Python 3.12.2
- OpenAI API Key
- Antrophic API Key

## Installation

1. Clone the repository:
   ```bash
   git https://github.com/Switchfleet/LLM_prueba.git
   
2. Install Poetry (if not already installed)

3. Install dependencies using Poetry:
   ```bash
   poetry install --no-root
      ```
4. Create a file called .env with the variables OPENAI_API_KEY and ANTHROPIC_API_KEY.
 
## Running the API

```bash
   poetry shell
   ```

```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
## Usage
Method: POST

Description: Extract vehicle specifications from a given vehicle description.

Request Body:
```bash
{
    "description": "Toyota Corolla 2023 Hybrid automatic"
}
```

You can use it from the docs url http://127.0.0.1:8000/docs. The method name is extract-specifications.





