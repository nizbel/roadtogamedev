from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Technology


class TechnologyAdmin(ModelAdmin):
    model = Technology
    menu_label = 'Techs'
    list_display = ("name",)
    list_filter = ("name",)


modeladmin_register(TechnologyAdmin)
