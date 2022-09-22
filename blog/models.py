from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db import models
from wagtail.core import blocks

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.search import index
from wagtailtrans.models import TranslatablePage


class BlogIndexPage(TranslatablePage):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        # Paginate all posts by 10 per page
        paginator = Paginator(blogpages, 10)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            blogpages = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            blogpages = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            blogpages = paginator.page(paginator.num_pages)
        context['blogpages'] = blogpages

        # Add specific class name
        BlogIndexPage.fill_blog_page_types(blogpages)

        return context

    @staticmethod
    def fill_blog_page_types(blog_pages):
        """
        Inserts page_type in each blog page
        :param blog_pages:
        :return none:
        """
        for blog_page in blog_pages:
            if isinstance(blog_page.specific, CommonPage):
                blog_page.page_type = blog_page.specific.category.name
            else:
                blog_page.page_type = blog_page.specific_class.__name__

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    parent_page_types = ['home.HomePage']
    subpage_types = ['blog.DevJournalPage', 'blog.GameAnalysisPage', 'blog.CommonPage']


class Category(models.Model):
    name = models.CharField("Name", max_length=30)

    class Meta:
        unique_together = ('name', )

    def __str__(self):
        return self.name

    def dummy_for_makemessages():
        """
        This function allows manage makemessages to find the forecast types for translation.
        Removing this code causes makemessages to comment out those PO entries, so don't do that
        unless you find a better way to do this
        """
        from django.utils.translation import ugettext_lazy as _, pgettext
        # pgettext('forecast type', 'Random')
        _("Random")

class CommonPage(TranslatablePage):
    date = models.DateField("Post date")
    category = models.ForeignKey("Category", on_delete=models.PROTECT)
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock(template="blocks/paragraph.html")),
    ])

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('category'),
        StreamFieldPanel('body', classname="full"),
    ]

    parent_page_types = ['blog.BlogIndexPage']
    subpage_types = []

    def first_paragraph(self):
        for block in self.body:
            if block.block_type == 'paragraph':
                return block.value


class DevJournalPage(TranslatablePage):
    date = models.DateField("Post date")
    entry_index = models.IntegerField("Entry index")
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock(template="blocks/paragraph.html")),
    ])

    class Meta:
        unique_together = ('entry_index', 'translatablepage_ptr_id')

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('entry_index'),
        FieldPanel('date'),
        StreamFieldPanel('body', classname="full"),
    ]

    parent_page_types = ['blog.BlogIndexPage']
    subpage_types = []

    def first_paragraph(self):
        for block in self.body:
            if block.block_type == 'paragraph':
                return block.value


class GameAnalysisPage(TranslatablePage):
    date = models.DateField("Post date")
    platform = models.CharField(max_length=30)
    release_year = models.PositiveSmallIntegerField()
    hours_sunk = models.PositiveSmallIntegerField()
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock(template="blocks/paragraph.html")),
        ('music_highlights', blocks.ListBlock(blocks.StructBlock([
            ('name', blocks.CharBlock(max_length=50)),
            ('url', blocks.URLBlock(required=False)),
        ]), template="blocks/music_highlights.html")),
        ('gameplay_mechanics', blocks.ListBlock(blocks.RichTextBlock(),
                                                template="blocks/gameplay_mechanics.html", icon='cogs')),
        ('learnings', blocks.ListBlock(blocks.RichTextBlock(),
                                       template="blocks/learnings.html", icon='tick')),
        ('memorable_moments', blocks.ListBlock(blocks.RichTextBlock(),
                                               template="blocks/memorable_moments.html", icon='pick')),
        ('stats', blocks.ListBlock(blocks.StructBlock([
            ('description', blocks.RichTextBlock()),
        ]), template="blocks/stats.html"))
    ])

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('platform'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('release_year'),
        FieldPanel('date'),
        FieldPanel('platform'),
        FieldPanel('hours_sunk'),
        StreamFieldPanel('body', classname="full"),
    ]

    def first_paragraph(self):
        for block in self.body:
            if block.block_type == 'paragraph':
                return block.value

    def music_highlights_count(self):
        for block in self.body:
            if block.block_type == 'music_highlights':
                return len(block.value)

    parent_page_types = ['blog.BlogIndexPage']
    subpage_types = []
