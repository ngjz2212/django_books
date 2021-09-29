from django.db import models
import datetime

class Book(models.Model):
    title = models.CharField("Title",max_length=200)
    author = models.CharField("Author",max_length=200)
    summary = models.TextField("Plot",blank=True,null=True)
    my_order = models.PositiveIntegerField("Rank",default=0, blank=True, null=True)
    pdf_file = models.FileField("File",blank=True,null=True)

    def __str__(self):
        return self.title

    def remove_on_pdf_file_update(self):
        try:
            # is the object in the database yet?
            obj = Book.objects.get(id=self.id)
        except Book.DoesNotExist:
            # object is not in db, nothing to worry about
            return
        # is the save due to an update of the actual pdf_file file?
        if obj.pdf_file and self.pdf_file and obj.pdf_file != self.pdf_file:
            # delete the old pdf_file file from the storage in favor of the new file
            obj.pdf_file.delete()

    def delete(self, *args, **kwargs):
        # object is being removed from db, remove the file from storage first
        self.pdf_file.delete()
        return super(Book, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # object is possibly being updated, if so, clean up.
        self.remove_on_pdf_file_update()
        return super(Book, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Books"
        ordering = ['my_order']

STATUS_CHOICES = [
    ('d', 'Draft'),
    ('p', 'Published'),
    ('w', 'Withdrawn'),
]

SERIES_CHOICES = [
    ('A1', 'A1'),
    ('A2', 'A2'),
    ('A3', 'A3'),
    ('A4', 'A4'),
    ('A5', 'A5'),
    ('A6', 'A6'),
    ('B1', 'B1'),
    ('B2', 'B2'),
    ('B3', 'B3')
]

class Publication(models.Model):
    date_submitted = models.DateField("Date Submitted",default=datetime.datetime.today)
    book_title = models.CharField("Book Title",max_length=200)
    priority_no = models.PositiveIntegerField("Order",default=0, blank=True, null=True)
    series = models.CharField("Series",max_length=2, choices=SERIES_CHOICES)
    publication_remarks = models.TextField("Remarks")
    status = models.CharField("Status",max_length=1, choices=STATUS_CHOICES, default='d')
    book_pdf = models.FileField("File",blank=True,null=True)

    def __str__(self):
        return self.book_title

    class Meta:
        verbose_name_plural = "Publications"
        ordering = ['priority_no']


