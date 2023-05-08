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
    daily_lbl: CreateTrafficResponseSensorValue
    monthly_lbl: CreateTrafficResponseSensorValue


def create_sensor_value(
    api_url: str,
    api_token: str,
    key: str,
    value: float,
    timestamp: str,
) -> CreateSensorValueResponse:
    res = requests.post(
        url=api_url, 
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
  daily_lbl: int,
  monthly_lbl: int,
  timestamp: str,
) -> CreateL12TrafficResult:
    sensor_value_daily_lbl = create_sensor_value(
        api_url=api_url,
        api_token=api_token,
        key='l12_traffic_daily_lbl',
        value=daily_lbl,
        timestamp=timestamp,
    )

    sensor_value_monthly_lbl = create_sensor_value(
        api_url=api_url,
        api_token=api_token,
        key='l12_traffic_monthly_lbl',
        value=monthly_lbl,
        timestamp=timestamp,
    )

    return CreateL12TrafficResult(
        daily_lbl=sensor_value_daily_lbl,
        monthly_lbl=sensor_value_monthly_lbl,
    )
