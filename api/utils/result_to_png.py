import os
from uuid import uuid4

import imgkit
from jinja2 import Template

from ..adapters import s3

_template = """
<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <style>
      @font-face {
        font-family: "StratosWeb";
        src: URL("/usr/app/api/utils/static/Stratos-Semibold.ttf")
          format("truetype");
      }

      body {
        width: 1200px;
        height: 630px;
        display: flex;
        position: relative;
        margin: 0;
      }
      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
      .wrapper {
        position: fixed;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      .rating {
        display: flex;
        align-items: center;
        text-align: center;
        justify-content: center;
        background-color: {{background_color}};
        border-radius: 230px;
        padding: 23px 69px;
        font-family: "StratosWeb", sans-serif;
        font-weight: bold;
        font-size: 134px;
        color: white;
        font-weight: 600;
        letter-spacing: -0.07em;
      }
    </style>
  </head>
  <body>
    <img
      src="{{background_url}}"
    />
    <div class="wrapper">
      <div class="rating">
        <span class="score">{{score}}</span>
        <span class="separator">/</span>
        <span class="max-score">{{max_score}}</span>
      </div>
    </div>
  </body>
</html>
"""

async def make(background_url: str, score, total_questions):
    try:
        successful_perc = score / total_questions
        if successful_perc >= 0.8:
            color = "#FF54C9"
        elif successful_perc >= 0.5:
            color = "#19D429"
        else:
            color = "#FFC759"    
        
        template = Template(_template).render(
            background_url=background_url,
            score=score,
            max_score=total_questions,
            background_color=color,
        )
        
        options = {"format": "png", "quality": 100, 'enable-local-file-access': None}
        extention = background_url.split("/")[-1].split(".")[-1]
        output = f"{uuid4()}.{extention}"
        
        print(f">>> {output}: Start rendering")
        result = imgkit.from_string(template, False, options=options)
        print(f">>> {output}: End rendering")
        file_path = f"invitation_img/{uuid4()}.png"
        url = await s3.upload_file(result, file_path)
        print(f">>> {output}: Uploaded")
        return url
        
    except Exception as e:
        print(f">>> {output}: Error", str(e))
    finally:
        try:
            os.remove(output)
        except OSError:
            pass
