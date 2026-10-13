import json
from typing import Literal
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    city : str = Field(
        description="要查询的城市名称，例如：上海，北京，Tokoyo"
        )
    unit : Literal["celsius", "fahrenheit"] = Field(
        default="celsius",
        description="温度单位，默认为摄氏度"
    )

schema = WeatherInput.model_json_schema()

print(json.dumps(schema, indent=2, ensure_ascii=False))

