from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, Field


class ServerStatus(Enum):
    offline = 0
    online = 1
    starting = 2
    stopping = 3
    restarting = 4
    saving = 5
    loading = 6
    crashed = 7
    pending = 8
    preparing = 10


class Account(BaseModel):
    name: str
    email: str
    verified: bool
    # the api docs say this is a "number" but it's actually a float
    credits: float


class ServerPlayers(BaseModel):
    max: int
    count: int
    list: list[str]


class ServerSoftware(BaseModel):
    id: str
    name: str
    version: str


class Server(BaseModel):
    id: str
    name: str
    address: str
    motd: str
    status: ServerStatus
    host: Optional[str]
    port: Optional[int]
    players: ServerPlayers
    software: Optional[ServerSoftware]
    shared: bool


class LogUpload(BaseModel):
    id: str
    url: str
    raw: str


class PathInfo(BaseModel):
    path: str
    name: str
    is_text_file: bool = Field(alias="isTextFile")
    is_config_file: bool = Field(alias="isConfigFile")
    is_directory: bool = Field(alias="isDirectory")
    is_log: bool = Field(alias="isLog")
    is_readable: bool = Field(alias="isReadable")
    is_writable: bool = Field(alias="isWritable")
    size: int
    children: Optional[list["PathInfo"]]


class ConfigOption(BaseModel):
    key: str
    value: Union[str, int, float, bool]
    label: str
    # this type defined the type of value
    type: str
    # options is used for select and multiselect types
    options: Optional[list[Union[str, int, float, bool]]]
