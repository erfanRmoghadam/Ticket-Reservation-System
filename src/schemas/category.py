from pydantic import BaseModel, ConfigDict


class CategoryCreateRequest(BaseModel):
    name: str
    description: str | None = None


class CategoryUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    category_id: int
    name: str
    description: str | None = None
