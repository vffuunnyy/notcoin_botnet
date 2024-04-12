from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel


BaseModel.model_config["arbitrary_types_allowed"] = True
BaseModel.model_config["populate_by_name"] = True
BaseModel.model_config["alias_generator"] = to_camel


class BaseWithWebDataReqeust(BaseModel):
    web_app_data: str = Field()


class ClickRequest(BaseWithWebDataReqeust):
    count: int = Field(0)
    hash: int | None = Field(None)
    turbo: bool | None = Field(None)


class PlausibleEventRequest(BaseModel):
    page: str = Field("pageview", alias="n")
    base_url: str = Field("clicker.joincommunity.xyz", alias="d")

    url: str = Field(..., alias="u")
    r: str | None = Field(None, alias="r")


class WebAppSessionRequest(BaseWithWebDataReqeust): ...
