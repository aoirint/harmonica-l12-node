import requests
from pydantic import BaseModel, parse_obj_as

import importlib.resources as ILR

CREATE_SENSOR_VALUE_QUERY = ILR.read_text('harmonica_l12_node', 'CreateSensorValue.graphql')


class CreateSensorValueRequest(BaseModel):
    key: str
    value: float
    timestamp: str


class CreateTrafficResponseSensorValue(BaseModel):
    id: str


class CreateSensorValueResponse(BaseModel):
    sensor_value: CreateTrafficResponseSensorValue


class CreateL12TrafficResult(BaseModel):
    daily: CreateTrafficResponseSensorValue
    monthly: CreateTrafficResponseSensorValue


def create_sensor_value(
    api_url: str,
    api_token: str,
    timeout: float,
    key: str,
    value: float,
    timestamp: str,
) -> CreateSensorValueResponse:
    res = requests.post(
        url=api_url, 
        timeout=timeout,
        headers={
            'Authorization': f'Bearer {api_token}',
        },
        json={
            'query': CREATE_SENSOR_VALUE_QUERY,
            'variables': CreateSensorValueRequest(
                key=key,
                value=value,
                timestamp=timestamp,
            ).dict(),
        },
    )
    res.raise_for_status()

    response_json = res.json()
    response_errors = response_json.get('errors')
    if response_errors:
        raise Exception(response_errors)

    response_data = response_json['data']
    return parse_obj_as(
        CreateSensorValueResponse,
        response_data,
    ).sensor_value


def create_l12_traffic(
  api_url: str,
  api_token: str,
  timeout: float,
  daily: int,
  monthly: int,
  timestamp: str,
) -> CreateL12TrafficResult:
    sensor_value_daily = create_sensor_value(
        api_url=api_url,
        api_token=api_token,
        timeout=timeout,
        key='l12_traffic_daily',
        value=daily,
        timestamp=timestamp,
    )

    sensor_value_monthly = create_sensor_value(
        api_url=api_url,
        api_token=api_token,
        timeout=timeout,
        key='l12_traffic_monthly',
        value=monthly,
        timestamp=timestamp,
    )

    return CreateL12TrafficResult(
        daily=sensor_value_daily,
        monthly=sensor_value_monthly,
    )
