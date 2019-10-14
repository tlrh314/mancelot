from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static


def set_meta_tags(request):
    page_title = "Mancelot"
    page_image = static("img/todo.png")
    page_description = "Mancelot: App voor Duurzame Mannenkleding"
    page_keywords = "Mancelot, 'duurzame kleding', app, duurzaam," + \
        " duurzame, mannenmode, 'Roman Markovski', 'Lorentz Stout'," + \
        " Verantwoord, 'verantwoorde kleding'"
    og_image = page_image
    og_title = page_title
    twitter_card = ""
    twitter_site = "@todo"  # Twitter Handle!
    twitter_title = page_title
    twitter_description = page_description
    twitter_image = page_image

    return {
        "page_title": page_title,
        "page_image": page_image,
        "page_title": page_title,
        "page_description": page_description,
        "page_keywords": page_keywords,
        "og_image": og_image,
        "og_title": og_title,
        "twitter_card": twitter_card,
        "twitter_title": twitter_title,
        "twitter_description": twitter_description,
        "twitter_image": twitter_image,
        "mancelot_kvk": settings.MANCELOT_KVK_NUMMER,
        "mancelot_btw": settings.MANCELOT_BTW_NUMMER,
    }
