import json

import pytest
from fastapi.exceptions import HTTPException

from src.services import get_question_answer_service
from tests.mocked_values import ai_response_gk, api_connection_error, prompt_gk_question


async def test_get_question_answer_service_success(mocker):
    response_payload = json.dumps(
        {
            "final_output": {
                "prompt": prompt_gk_question,
                "weather_response": ai_response_gk,
            }
        },
    )

    mock_run_result = mocker.MagicMock()
    mock_run_result.final_output = json.dumps(response_payload)
    mocker.patch(
        "src.services.question_answer_service.generate_session",
        return_value="session-123",
    )
    mocked_service = mocker.patch(
        "src.services.question_answer_service.Runner.run", return_value=mock_run_result
    )

    mocked_prompt = mocker.Mock()
    mocked_prompt.prompt = prompt_gk_question
    result = await get_question_answer_service(mocked_prompt)
    print("result", result)
    mocked_service.assert_called()


async def test_get_question_answer_service_failure(mocker):
    mock_error_result = api_connection_error

    mocked_service = mocker.patch("src.services.question_answer_service.Runner.run")
    mocked_service.side_effect = Exception(mock_error_result)

    mocked_prompt = mocker.Mock()
    mocked_prompt.prompt = prompt_gk_question
    with pytest.raises(HTTPException) as error_info:
        await get_question_answer_service(mocked_prompt)

    assert error_info.value.status_code == 500
    mocked_service.assert_called_once()
