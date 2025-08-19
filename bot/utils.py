import re
import string
from django.conf import settings

def create_post(**kwargs):
    return {
        "text": settings.SEND_ADMIN_POST.format(**kwargs),
        "reply_markup": settings.SEND_ADMIN_MARKUP,
        "chat_id": settings.ADMIN_TELEGRAM_ID,
        "disable_web_page_preview": True,
        "parse_mode": "HTML"
    }

def parse_formatted_message(message: str) -> dict:
    """
    Template asosida message ichidan qiymatlarni ajratib oladi.
    """
    template = settings.SEND_ADMIN_POST
    # template html to simple text
    template = template.replace("<b>", "").replace("</b>", "").replace("<i>", "").replace("</i>", "").replace("</code>", "").replace("<code>", "")
    # Template bo'yicha regex pattern yasash
    regex_pattern = re.escape(template)

    # {field} larni regex guruhlariga almashtiramiz
    field_names = []
    for literal_text, field_name, format_spec, conversion in string.Formatter().parse(template):
        if field_name is not None:
            field_names.append(field_name)
            regex_pattern = regex_pattern.replace(
                re.escape("{" + field_name + "}"), r"(.+?)"
            )

    # Regex orqali moslashtiramiz
    match = re.match(regex_pattern, message, re.DOTALL)
    if not match:
        return {}

    values = match.groups()
    return dict(zip(field_names, values))



if __name__ == "__main__":

    parsed = parse_formatted_message(create_post("Bexruz", "+998901234567", "123456789"))
    print(parsed)



