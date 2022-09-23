from django.db import models
from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
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


class Technology(models.Model):
    name = models.CharField("Name", max_length=30)

    class Meta:
        unique_together = ('name',)

    def __str__(self):
        return self.name


class PortfolioPage(TranslatablePage):
    parent_page_types = ['home.HomePage']
    subpage_types = ['home.GamePage', 'home.ResumePage']

    def get_context(self, request):
        # Update context to include games
        context = super().get_context(request)
        games = self.get_children().live()

        context['games'] = games
        return context

    parent_page_types = ['home.HomePage']
    subpage_types = ['home.GamePage', 'home.ResumePage']


class GamePage(TranslatablePage):
    short_description = RichTextField()
    development_period = models.CharField("Development Period", max_length=30)

    body = StreamField([
        ('paragraph', blocks.RichTextBlock(template="blocks/paragraph.html")),
        ('award', blocks.RichTextBlock(template="blocks/paragraph.html")),
        ('problem', blocks.RichTextBlock(template="blocks/paragraph.html")),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('development_period'),
        FieldPanel('short_description'),
        StreamFieldPanel('body', classname="full"),
    ]

    parent_page_types = ['home.PortfolioPage']
    subpage_types = []


class ResumePage(TranslatablePage):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    parent_page_types = ['home.PortfolioPage']
    subpage_types = []
