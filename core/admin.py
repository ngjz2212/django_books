from django.contrib import admin
from datetime import datetime
from core.models import Book, Author, Publication, STATUS_CHOICES, SERIES_CHOICES
from django.http import HttpResponse
from django.forms import ModelForm
from django import forms
import csv
# Register your models here.

def export_to_csv(self, request, queryset):
    meta = self.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])

    return response
export_to_csv.short_description = 'Export to CSV'  #short description

admin.site.add_action(export_to_csv) ## Apply function globally


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):    
    list_display = ["title","isbn","author","summary"]
    list_filter = ["author",]
    list_per_page = 250
    search_fields = ["title__startswith", ]
    fields = ["title","isbn","author",]

    actions = ["publish"]
    def publish(modeladmin, request, queryset):
        for book in queryset:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            p = Publication(release_no=timestamp,isbn=book.isbn,title=book.title,publication_remarks=book.summary)
            p.save()
    publish.short_description = "Draft selected books for publication"


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["author_id","name","writing_level","publisher_id"]
    list_filter = ["publisher_id"]
  

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    actions = ["make_published","make_withdrawn"]
    def make_published(modeladmin, request, queryset):
        queryset.update(status='p')
    make_published.short_description = "Publish selected books"

    def make_withdrawn(modeladmin, request, queryset):
        queryset.update(status='w')
    make_withdrawn.short_description = "Withdraw selected books"


    def formfield_for_choice_field(self, db_field, request, **kwargs):
        curr_user = request.user.username
        if db_field.name == "series":
            if curr_user.startswith('A'):
                kwargs['choices'] = SERIES_CHOICES[:6]
            if curr_user.startswith('B'):
                kwargs['choices'] = SERIES_CHOICES[6:] 
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    list_display = ["release_no","isbn","title","publication_remarks","status"]
    list_filter = ["release_no"]


