import imgkit
import httpx
from jinja2 import Template
from uuid import uuid4
import os
from ..adapters import s3


_template = """
<!DOCTYPE html>
<html lang="ru">
    <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Динамическое изображение</title>
    <style>
        @font-face {
        font-family: "StratosWeb";
        src: URL("api/utils/static/Stratos-Semibold.ttf") format("truetype");
        }

        body {
        width: 1200px;
        height: 630px;
        display: flex;
        position: relative;
        }
        img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        }
        div {
        position: absolute;
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        }
        span{
        font-family: "StratosWeb", sans-serif;
        font-size: 103px;
        letter-spacing: -0.07em;
        color: white;
        padding: 23px 69px;
        background-color: {background_color};
        border-radius: 230px;
        }
    </style>
    </head>
    <body>
    <img
        src="{background_url}"
    />
    <div>
        <span>{score}/{total_questions}</span>
    </div>
    </body>
</html>
"""


async def download_image(image_url, save_path="image.jpg"):
    async with httpx.AsyncClient() as client:
        response = await client.get(image_url)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            for chunk in response.iter_bytes(1024):
                file.write(chunk)
        return save_path
    raise ValueError(f"Cannot download {image_url}")


def html_to_png(html_content, output_path="output.png"):
    """Конвертирует HTML в PNG"""

    print(f"PNG сохранен: {output_path}")


async def make(
    invitation_id, background_url: str, score, total_questions
):
    try:
        successful_perc = score / total_questions
        if successful_perc >= 8:
            color = "#FF54C9"
        elif successful_perc >= 5:
            color = "#19D429"
        else :
            color = "#FFC759"    
        
        extention = background_url.split("/")[-1].split(".")[-1]
        temp_path = f"{uuid4()}.{extention}"
        output_path = "output_" + temp_path
        print('Trying to download', background_url)
        local_filepath = await download_image(background_url, save_path=temp_path)
        print("downloaded")
        template = Template(_template).render(
            background_url=local_filepath,
            score=score,
            total_questions=total_questions,
            background_color=color,
        )
        print("rendered")
        options = {"format": "png", "quality": 100}
        imgkit.from_string(template, output_path, options=options)
        print("made")
        with open(output_path, "rb") as file:
            file_path = f"invitations/{invitation_id}.png"
            s3.upload_file(file.read(), file_path)
            print("uploaded")
            return file_path

    except Exception as e:
        print(e)
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass
        try:
            os.remove(output_path)
        except OSError:
            pass
