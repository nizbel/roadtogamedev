from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtailtrans.models import TranslatablePage

from blog.models import BlogIndexPage


class HomePage(TranslatablePage):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blog = self.get_children().get(slug="blog")
        blog_pages = blog.get_children().live().order_by('-first_published_at')[:3]

        BlogIndexPage.fill_blog_page_types(blog_pages)

        context['blogpages'] = blog_pages
        return context


class AboutMePage(TranslatablePage):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    parent_page_types = ['home.HomePage']
    subpage_types = []
