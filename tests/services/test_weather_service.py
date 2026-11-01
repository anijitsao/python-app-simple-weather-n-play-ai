import json

import pytest
from fastapi.exceptions import HTTPException

from src.services import get_weather_service
from tests.mocked_values import (
    ai_response_weather,
    api_connection_error,
    city,
    prompt_weather,
)


async def test_get_weather_service_success(mocker):
    response_payload = json.dumps(
        {
            "final_output": {
                "prompt": prompt_weather,
                "weather_response": ai_response_weather,
            }
        },
    )

    mock_run_result = mocker.MagicMock()
    mock_run_result.final_output = json.dumps(response_payload)

    mocked_service = mocker.patch(
        "src.services.weather_service.Runner.run", return_value=mock_run_result
    )
    result = await get_weather_service(city)
    print("result", result)
    mocked_service.assert_called_once()


async def test_get_weather_service_failure(mocker):
    mock_error_result = api_connection_error

    mocked_service = mocker.patch("src.services.weather_service.Runner.run")
    mocked_service.side_effect = Exception(mock_error_result)

    with pytest.raises(HTTPException) as error_info:
        await get_weather_service(city)

    assert error_info.value.status_code == 500
    mocked_service.assert_called_once()
