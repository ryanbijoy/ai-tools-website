from django.contrib import admin
from .models import AiTool, ToolRating, Testimonial, Category
from import_export.admin import ImportExportModelAdmin


@admin.action(description="Mark selected as Affiliate Present")
def affiliate_present(modeladmin, request, queryset):
    queryset.update(affiliate_link=True)


@admin.action(description="Mark Category as Active")
def category_status(modeladmin, request, queryset):
    queryset.update(active=True)


@admin.register(AiTool)
class AiToolAdmin(ImportExportModelAdmin):
    list_display = ('ai_tool', 'description', 'features', 'about', 'affiliate_link')
    ordering = ('ai_tool',)
    actions = [affiliate_present]


@admin.register(ToolRating)
class ToolRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'ai_tool', 'star_rating', "review")


@admin.register(Category)
class ToolCategory(ImportExportModelAdmin):
    list_display = ('id', 'title', 'active')
    actions = [category_status]
