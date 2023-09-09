import traceback
import uuid
from pathlib import Path
from typing import Union, overload

import plotly.graph_objects as go
import plotly.io as pio

from models.api_models import PlotsResponse

from .backend import pywry_backend


class PyWryFigure(go.Figure):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def show(self, *args, **kwargs):
        if pywry_backend().isatty:
            try:
                # We send the figure to the backend to be displayed
                return pywry_backend().send_figure(self)
            except Exception:
                traceback.print_exc()

        return pio.show(self, *args, **kwargs)

    @overload
    def update(self, *args, **kwargs) -> "PyWryFigure":
        pass

    def update(self, *args, **kwargs) -> "PyWryFigure":
        super().update(*args, **kwargs)

        return self

    @overload
    def update_layout(self, *args, **kwargs) -> "PyWryFigure":
        pass

    def update_layout(self, *args, **kwargs) -> "PyWryFigure":
        super().update_layout(*args, **kwargs)

        return self

    def pywry_image(
        self,
        filepath: Union[str, Path] = "plotly_image.png",
        scale: int = 1,
        timeout: int = 5,
    ) -> bytes:
        """Return image as bytes or save to file.

        filepath : Union[str, Path], optional
            Filepath to save image to, by default "plotly_image.png"
        scale : int, optional
            Image scale, by default 1
        timeout : int, optional
            Timeout for receiving the image, by default 5
        """

        if not isinstance(filepath, Path):
            filepath = Path(filepath)

        img_format = filepath.suffix.lstrip(".").lower()

        if img_format == "jpg":
            img_format = "jpeg"

        if img_format not in ["png", "jpeg", "svg"]:
            raise ValueError(
                f"Invalid image format {img_format}. "
                "Must be one of 'png', 'jpeg', or 'svg'."
            )

        try:
            response = pywry_backend().figure_write_image(
                self,
                img_format=img_format,
                scale=scale,
                timeout=timeout,
            )

            if img_format == "svg":
                return filepath.write_bytes(response)

            return response

        except Exception:
            traceback.print_exc()

    def prepare_image(
        self,
        filename: str = "plots",
        add_uuid: bool = True,
    ) -> PlotsResponse:
        """Prepare image for sending to Discord.

        Parameters
        ----------
        filename : str
            Name to save image as
        add_uuid : bool, optional
            Add uuid to filename, by default True

        Returns
        -------
        PlotsResponse
            PlotsResponse dataclass model with filename, image64
        """
        filename_uuid = (
            f"{filename}_{str(uuid.uuid4()).replace('-', '')}" if add_uuid else filename
        )

        return PlotsResponse(filename=filename_uuid, image64=self.pywry_image(scale=1))
