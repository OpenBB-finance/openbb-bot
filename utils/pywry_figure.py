import base64
import io
import traceback
import uuid
from pathlib import Path
from typing import Union, overload

import plotly.graph_objects as go
import plotly.io as pio
from PIL import Image

from models.api_models import PlotsResponse

from .backend import pywry_backend

BOT_PATH = (Path(__file__).parent.parent / "bot").resolve()


def autocrop_image(image: Image.Image, border=0) -> Image.Image:
    """Crop empty space from PIL image

    Parameters
    ----------
    image : Image.Image
        PIL image to crop
    border : int, optional
        scale border outwards, by default 0

    Returns
    -------
    Image.Image
        Cropped image
    """
    bbox = image.getbbox()
    image = image.crop(bbox)
    (width, height) = image.size
    width += border * 2
    height += border * 2
    cropped_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    cropped_image.paste(image, (border, border))
    return cropped_image


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

        fig_img = Image.open(io.BytesIO(base64.b64decode(self.pywry_image(scale=1))))
        im_bg = Image.open(BOT_PATH / "assets" / "bg_dark_charts.png")

        # make new transparent image
        new_img = Image.new("RGBA", im_bg.size, (255, 255, 255, 0))

        # paste background on it
        new_img.paste(im_bg, (0, 0), im_bg)

        # Paste fig onto background img
        x1 = int(0.5 * new_img.size[0]) - int(0.5 * fig_img.size[0])
        y1 = int(0.5 * new_img.size[1]) - int(0.5 * fig_img.size[1])
        x2 = int(0.5 * new_img.size[0]) + int(0.5 * fig_img.size[0])
        y2 = int(0.5 * new_img.size[1]) + int(0.5 * fig_img.size[1])

        new_img.paste(fig_img, box=(x1, y1 - 15, x2, y2 - 15))

        paste = Image.open(BOT_PATH / "assets" / "bg_charts_paste.png")
        new_img.paste(paste, (0, 0), paste)

        fig_img.close()
        im_bg.close()
        paste.close()

        imagebytes = io.BytesIO()
        new_img.save(imagebytes, "PNG")
        new_img.close()
        imagebytes.seek(0)

        return PlotsResponse(
            filename=filename_uuid,
            image64=base64.b64encode(imagebytes.read()).decode("utf-8"),
        )

    def prepare_table(
        self,
        filename: str = "plots",
        add_uuid: bool = True,
    ) -> PlotsResponse:
        filename_uuid = (
            f"{filename}_{str(uuid.uuid4()).replace('-', '')}" if add_uuid else filename
        )

        image = autocrop_image(
            Image.open(io.BytesIO(base64.b64decode(self.pywry_image(scale=2)))), 0
        )

        imagebytes = io.BytesIO()
        image.save(imagebytes, "PNG")
        image.close()
        imagebytes.seek(0)

        return PlotsResponse(
            filename=filename_uuid,
            image64=base64.b64encode(imagebytes.read()).decode("utf-8"),
        )
