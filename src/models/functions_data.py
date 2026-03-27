from pydantic import BaseModel


class ParameterTypeModel(BaseModel):
    type: str


class FunctionModel(BaseModel):
    name: str
    description: str
    parameters: dict[str, ParameterTypeModel]
    returns: ParameterTypeModel
