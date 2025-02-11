import imgkit
from jinja2 import Template

# HTML шаблон с динамическими параметрами
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Динамическое изображение</title>
    <style>
        body {
            width: 600px;
            height: 400px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background-color: {{ background_color }};
            font-family: Arial, sans-serif;
        }
        img {
            max-width: 100%;
            max-height: 200px;
        }
        p {
            font-size: 20px;
            color: white;
        }
    </style>
</head>
<body>
    <img src="{{ image_url }}" alt="Dynamic Image">
    <p>{{ text }}</p>
</body>
</html>
"""

def render_html(image_url, text, background_color):
    """Генерирует HTML-код с подставленными параметрами."""
    template = Template(HTML_TEMPLATE)
    return template.render(image_url=image_url, text=text, background_color=background_color)

def html_to_png(html_content, output_path="output.png"):
    """Конвертирует HTML в PNG."""
    options = {
        'format': 'png',
        'quality': 100
    }
    imgkit.from_string(html_content, output_path, options=options)
    print(f"PNG сохранен: {output_path}")

# Динамические параметры
image_url = "https://storage.yandexcloud.net/quiz-bot-web/question_pics/6e2d2336-8741-4493-9eea-63e933bc5abe.png"
text = "Привет, это тест!"
background_color = "#3498db"

# Генерация HTML и конвертация в PNG
html_content = render_html(image_url, text, background_color)
html_to_png(html_content)
