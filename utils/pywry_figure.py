from pathlib import Path
from typing import Union

import plotly.graph_objects as go
import plotly.io as pio

from models.api_models import PlotsResponse
from utils.helpers import uuid_get

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
                pass

        return pio.show(self, *args, **kwargs)

    def pywry_write_image(
        self,
        filepath: Union[str, Path] = "plotly_image.png",
        scale: int = 1,
        timeout: int = 5,
    ):
        """Convert a Plotly figure to an image.

        filepath : Union[str, Path], optional
            Filepath to save image to, by default "plotly_image.png"
        scale : int, optional
            Image scale, by default 1
        timeout : int, optional
            Timeout for receiving the image, by default 5
        to_bytes : bool, optional
            Whether to return the image as bytes, by default False
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
            # We send the figure to the backend to be converted to an image
            response = pywry_backend().figure_write_image(
                self,
                img_format=img_format,
                scale=scale,
                timeout=timeout,
            )

            if img_format == "svg":
                return filepath.write_bytes(response)

            return response

        except Exception as e:
            print(e)
            pass

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
        filename_uuid = f"{filename}_{uuid_get()}" if add_uuid else filename

        plots_data = PlotsResponse(
            filename=filename_uuid, image64=self.pywry_write_image(scale=1)
        )

        return plots_data
