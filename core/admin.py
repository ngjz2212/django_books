from django.contrib import admin
from datetime import datetime
from core.models import Book, Author, Publication, STATUS_CHOICES, SERIES_CHOICES
from django.http import HttpResponse
from django.forms import ModelForm
from django import forms
import csv
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.http import HttpResponseRedirect

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
    
    def publish(self, request, queryset):
        # All requests here will actually be of type POST 
        # so we will need to check for our special key 'apply' 
        # rather than the actual request type
        if 'apply' in request.POST:
            # The user clicked submit on the intermediate form.
            # Perform our update action:
            priority_list = request.POST.copy().pop('_selected_action')
            print(priority_list)
            for book in queryset:
                priority = priority_list.index(str(book.pk)) + 1
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                p = Publication(priority_no=priority,release_no=timestamp,isbn=book.isbn,title=book.title,publication_remarks=book.summary,series='A1')
                p.save()
            
            # Redirect to our admin view after our update has 
            # completed with a nice little info message saying 
            # our models have been updated:
            self.message_user(request, "Successfully published {} books".format(queryset.count()))
            return HttpResponseRedirect(request.get_full_path())
                        
        return render(request,
                      'admin/order_intermediate.html',
                      context={'orders':queryset})
        
    publish.short_description = "Draft selected books for publication"

    change_list_template = "admin/change_list_filter_sidebar.html"

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

    list_display = ["title","priority_no","release_no","isbn","publication_remarks","status","series"]
    list_editable = ["priority_no",'status','series']
    list_filter = ["release_no"]