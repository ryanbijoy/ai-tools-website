from django.contrib import admin
from .models import AiTool, ToolRating, Testimonial
from import_export.admin import ImportExportModelAdmin


@admin.action(description="Mark selected as Affiliate Present")
def affiliate_present(modeladmin, request, queryset):
    queryset.update(affiliate_link=True)


@admin.register(AiTool)
class AiToolAdmin(ImportExportModelAdmin):
    list_display = ('ai_tool', 'category', 'description', 'features', 'about', 'affiliate_link')
    ordering = ('ai_tool',)
    actions = [affiliate_present]


@admin.register(ToolRating)
class ToolRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'ai_tool', 'star_rating', "review")


admin.site.register(Testimonial)
