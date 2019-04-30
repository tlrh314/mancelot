from django.contrib.staticfiles.templatetags.staticfiles import static

# from about.models import ContactInfo


class ContactInfoDefault(object):
    def __init__(self):
        """ Hardcoded in case there is no ContactInfo object """

        self.contact_email = "info@mancelot.nl"


def set_contactinfo(request):
    contactinfo = None  # ContactInfo.objects.first()
    if not contactinfo:
        contactinfo = ContactInfoDefault()

    return { "contact_email": contactinfo.contact_email }


def set_meta_tags(request):
    page_title = "Mancelot"
    page_image = static("img/todo.png")
    page_description = "Mancelot: App voor Duurzame Mannenkleding"
    page_keywords = "mannen, kleding, duurzame mannenkleding, eerlijke mannenkleding, conscious clothing"
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
    }
