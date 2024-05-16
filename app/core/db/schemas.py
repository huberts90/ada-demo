from pydantic import BaseModel


class OwnerSchema(BaseModel):
    id: int
    name: str


class RepositorySchema(BaseModel):
    id: int
    name: str
    owner_id: int

    class ConfigDict:
        from_attributes = True
