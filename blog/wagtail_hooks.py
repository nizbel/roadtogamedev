from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.core import hooks

from .models import Category


@hooks.register('register_rich_text_features')
def register_code_feature(features):
    features.default_features.append('code')


class CategoryAdmin(ModelAdmin):
    model = Category
    menu_label = 'Categories'
    list_display = ("name",)
    list_filter = ("name",)


modeladmin_register(CategoryAdmin)
