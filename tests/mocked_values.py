import ingestion

city = "Kolkata"
prompt_weather = f"What is the weather of {city}?"
ai_response_weather = {"temperature": 28.3, "is_day": 1}

prompt_gk_question = "Please describe python"
ai_response_gk = "Python is an programming languages used to create AI applications"

api_connection_error = "Unable to connect the API"
parsed_chunks = [{"content": ["chunk1"], "page_number": 1}]
ingestion_error = "Unable to insert chunks in vector db"
