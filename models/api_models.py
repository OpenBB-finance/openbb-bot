from typing import List, Optional

from pydantic import BaseModel


class PlotsResponse(BaseModel):
    """Contains plots data.

    filename : str
        Filename of the plot
    image64 : str
        Base64 encoded image
    """

    filename: str
    image64: bytes

    def to_dict(self):
        return self.dict()

    def to_json(self):
        return {k: v for k, v in self.dict().items() if v is not None}


class EmbedField(BaseModel):
    """Embed fields for Discord"""

    title: Optional[str] = ""
    description: Optional[str] = ""
    inline: Optional[bool] = False
    footer: Optional[str] = ""
    thumbnail: Optional[str] = ""
    homepage: Optional[str] = ""


class MainModel(BaseModel):
    title: Optional[str] = ""
    description: Optional[str] = ""
    embeds: List[EmbedField] = None
    images_list: List[str] = None
    plots: Optional[PlotsResponse] = None
