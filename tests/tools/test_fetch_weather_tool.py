import json

from agents.testing import ScriptedModel, assistant_message, function_call

from agents import Agent, RunConfig, Runner
from src.tools import fetch_weather
from tests.mocked_values import ai_response_weather, city


async def test_fetch_weather_success(mocker):
    model = ScriptedModel(
        [
            [function_call("fetch_weather", {"city": city}, call_id="call_1")],
            # assistant message takes only string no JSON in scripted model
            [assistant_message(json.dumps(ai_response_weather))],
        ]
    )
    weather_agent = Agent(name="WeatherAgent", model=model, tools=[fetch_weather])

    result = await Runner.run(
        weather_agent,
        f"What is the weather in {city}?",
        run_config=RunConfig(tracing_disabled=True),
    )

    assert result.final_output == json.dumps(ai_response_weather)
    model.assert_complete()
