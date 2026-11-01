from tests.mocked_values import (
    ai_response_gk,
    ai_response_weather,
    city,
    prompt_gk_question,
    prompt_weather,
)


def test_question_route_success(app_client, mocker):
    success_response = {
        "data": {"prompt": prompt_gk_question, "response": ai_response_gk}
    }
    mocked_service = mocker.patch(
        "src.routes.ai_routes.get_question_answer_service",
        return_value=success_response,
    )

    result = app_client.post("/question", json={"prompt": prompt_gk_question})
    assert result.status_code == 200
    # print(result.json())
    assert result.json()["data"]["response"] == ai_response_gk
    mocked_service.assert_called_once()


def test_question_route_service_validation_error(app_client):
    result = app_client.post("/question")

    assert result.status_code == 422


def test_get_weather_route_success(app_client, mocker):
    success_response = {
        "data": {"prompt": prompt_weather, "response": ai_response_weather}
    }
    mocked_service = mocker.patch(
        "src.routes.ai_routes.get_weather_service",
        return_value=success_response,
    )

    result = app_client.get(f"/get-weather/{city}")
    assert result.status_code == 200
    assert result.json()["data"]["response"] == ai_response_weather
    mocked_service.assert_called_once()


def test_weather_route_service_validation_error(app_client):
    result = app_client.get("/get-weather/")

    assert result.status_code == 404
