import base64
import io
import re

import disnake
import ujson

from bot.config import settings as cfg
from models.api_models import MainModel


class ShowView:
    """Class to create a view for the bot to send to the user

    Methods
    -------
    `create_response`:
        Creates the view and sends it to the user
    `discord`:
        Log data and process it to create a view for the bot to send to the user
    """

    async def create_response(
        self, inter: disnake.AppCmdInter, data: MainModel, no_embed: bool = False
    ):
        """Creates the view and sends it to the user

        Parameters
        ----------
        inter : `class`
            The discord interface class
        data : `dict`
            The data from the API to be used in the view
        """

        try:
            data = MainModel(**data)
            embed = disnake.Embed(
                title=data.title, colour=cfg.COLOR, description=data.description
            )
            embed.set_author(name=cfg.AUTHOR_NAME, icon_url=cfg.AUTHOR_ICON_URL)

            if data.embeds is not None:
                for field in data.embeds:
                    if field.homepage:
                        embed.url = field.homepage
                    if field.thumbnail:
                        embed.set_thumbnail(url=field.thumbnail)
                    if field.footer:
                        embed.set_footer(text=field.footer)
                    if field.title and field.description:
                        embed.add_field(
                            name=field.title,
                            value=field.description,
                            inline=field.inline,
                        )

            if data.plots is not None:
                filename = data.plots.filename[0:10]
                image64 = base64.b64decode(data.plots.image64)
                b64bytes = io.BytesIO(image64)
                image = disnake.File(b64bytes, filename=f"{filename}.png")
                embed.set_image(url=f"attachment://{filename}.png")

                try:
                    if not no_embed:
                        await inter.send(embed=embed, file=image)
                    else:
                        await inter.send(data.description, file=image)
                except disnake.errors.DiscordServerError:
                    await inter.send(
                        "Discord server error while sending image, try again later"
                    )

                return image.close()

            return await inter.send(embed=embed)
        except Exception as e:
            print(e)
            raise Exception("No data Found") from e

    async def discord(
        self,
        inter: disnake.AppCmdInter,
        cmd_name: str,
        data: dict,
        error: bool = False,
        no_embed: bool = False,
    ):
        """Process data and create a view to respond to the user

        Parameters
        ----------
        inter : `class`
            The discord interface class
        cmd_name : `str`
            The command used to call the view
        data : `dict`
            The data from the API to be used in the view
        error : `bool`
            Whether or not the data is an error
        no_embed : `bool`
            Whether or not to use an embed
        """
        try:
            if error:
                raise Exception(ujson.loads(data)["exception"])

            await self.create_response(inter, data, no_embed)

        except Exception as e:
            print(str(e).replace("|", "-"))
            try:
                error_msg = str(e).replace("\n", "")
                error_str = re.search(
                    r"\w*\:\s(\w.*)", error_msg.rsplit("|", maxsplit=1)[-1]
                ).group(1)
            except Exception as e:
                error_str = "No data Found"

            embed = disnake.Embed(
                title=cmd_name, colour=cfg.COLOR, description=error_str
            )
            embed.set_author(name=cfg.AUTHOR_NAME, icon_url=cfg.AUTHOR_ICON_URL)

            await inter.send(embed=embed, delete_after=10)
