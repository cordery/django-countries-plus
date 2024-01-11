from django.contrib import admin

from sample_app.models import Company


class CompanyAdmin(admin.ModelAdmin):
    autocomplete_fields = ["country"]


admin.site.register(Company, CompanyAdmin)
