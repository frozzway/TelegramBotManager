from typing import Literal

from pydantic import BaseModel, Field, HttpUrl, field_serializer


__all__ = ['CategoryBase', 'Category', 'LinkButtonBase', 'LinkButton', 'ScenarioButton', 'Ownership']


class CategoryBase(BaseModel):
    name: str = Field(description='Наименование категории (заголовок)')
    text: str | None = Field(default=None, description='Текст категории')
    tree_header: bool = Field(default=False, description='Флаг вывода наименования категории с наименованием родителя')
    page_size: int | None = Field(default=None, gt=2, description='Количество кнопок на одной странице категории (при пагинации)')


class Category(CategoryBase):
    id: int


class LinkButtonBase(BaseModel):
    name: str = Field(description='Текст кнопки')
    url: HttpUrl = Field(description='Адрес URL')

    @field_serializer('url')
    def serialize_url(self, url: HttpUrl) -> str:
        return str(url)


class LinkButton(LinkButtonBase):
    id: int


class ScenarioButton(BaseModel):
    id: int
    name: str = Field(description='Текст кнопки')


class Ownership(BaseModel):
    element_type: Literal['Category', 'LinkButton', 'ScenarioButton'] = Field(description='Тип элемента')
    element_id: int = Field(description='Идентификатор элемента')