from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.blocks import ImageChooserBlock
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


class Technology(TaggedItemBase):
    content_object = ParentalKey(
        'GamePage',
        related_name='tech_tags',
        on_delete=models.PROTECT,
    )


class PortfolioPage(TranslatablePage):
    parent_page_types = ['home.HomePage']
    subpage_types = ['home.GamePage']

    def get_context(self, request):
        # Update context to include games
        context = super().get_context(request)
        games = self.get_children().live()

        context['games'] = games
        return context


class GamePage(TranslatablePage):
    short_description = RichTextField()
    development_period = models.CharField('Development Period', max_length=30)
    tags = ClusterTaggableManager(through=Technology, blank=True)
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # Media
    itch_url = models.URLField('itch.io URL', blank=True)
    youtube_url = models.URLField('Youtube URL', blank=True)

    body = StreamField([
        ('paragraph', blocks.RichTextBlock(template="blocks/paragraph.html")),
        ('award', blocks.RichTextBlock(template="blocks/paragraph.html")),
        ('problem', blocks.RichTextBlock(template="blocks/paragraph.html")),
    ])

    images = StreamField([
        ('image', ImageChooserBlock('image'))
    ])

    content_panels = Page.content_panels + [
        FieldPanel('development_period'),
        FieldPanel('tags'),
        FieldPanel('short_description'),
        FieldPanel('main_image'),
        FieldPanel('itch_url'),
        FieldPanel('youtube_url'),
        StreamFieldPanel('body', classname="full"),
        StreamFieldPanel('images'),
    ]

    parent_page_types = ['home.PortfolioPage']
    subpage_types = []


class ResumePage(TranslatablePage):
    name = models.CharField('Name', max_length=50)
    email = models.CharField('Email', max_length=30)
    location = models.CharField('Location', max_length=30)
    phone = models.CharField('Phone', max_length=30)
    objective = RichTextField()

    pdf_file = models.ForeignKey(
        'wagtaildocs.Document', blank=True, null=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    skills = StreamField([
        ('skill_group', blocks.ListBlock(blocks.StructBlock([
            ('group_description', blocks.CharBlock(max_length=30)),
            ('skills', blocks.ListBlock(blocks.CharBlock(max_length=30))),
        ]), template="blocks/resume_skills.html")),
    ])
    experience = StreamField([
        ('experience', blocks.ListBlock(blocks.StructBlock([
            ('title_company', blocks.CharBlock(max_length=30)),
            ('period', blocks.CharBlock(max_length=30)),
            ('job_title', blocks.CharBlock(max_length=50)),
            ('attributions', blocks.ListBlock(blocks.RichTextBlock())),
        ]), template="blocks/resume_experience.html")),
    ])
    education = StreamField([
        ('education', blocks.ListBlock(blocks.StructBlock([
            ('institution', blocks.CharBlock(max_length=30)),
            ('period', blocks.CharBlock(max_length=30)),
            ('degree', blocks.CharBlock(max_length=50)),
        ]), template="blocks/resume_education.html")),
    ])
    side_projects = StreamField([
        ('side_projects', blocks.ListBlock(blocks.StructBlock([
            ('name', blocks.CharBlock(max_length=30)),
            ('period', blocks.CharBlock(max_length=30)),
            ('description', blocks.RichTextBlock()),
        ]), template="blocks/resume_side_projects.html")),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('email'),
        FieldPanel('location'),
        FieldPanel('phone'),
        FieldPanel('objective'),
        FieldPanel('pdf_file'),

        StreamFieldPanel('skills', classname="full"),
        StreamFieldPanel('experience', classname="full"),
        StreamFieldPanel('education', classname="full"),
        StreamFieldPanel('side_projects', classname="full"),
    ]

    parent_page_types = ['home.HomePage']
    subpage_types = []
