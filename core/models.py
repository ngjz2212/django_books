from django.db import models

class Author(models.Model):
    author_id = models.CharField("Author ID",max_length=200)
    name = models.CharField("Name",max_length=200)
    writing_level = models.IntegerField("Writing Level")
    publisher_id = models.CharField("Publisher ID",max_length=200)

    def __str__(self):
        return self.name

class Book(models.Model):
    author = models.CharField("Author",max_length=200)
    isbn = models.CharField("ISBN",max_length=200)
    title = models.CharField("Title",max_length=200)
    summary = models.TextField("Plot")
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.title

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
    priority_no = models.PositiveIntegerField(default=0, blank=False, null=False)
    release_no = models.CharField("Release No",max_length=200)
    series = models.CharField(max_length=2, choices=SERIES_CHOICES)
    isbn = models.CharField("ISBN",max_length=200)
    title = models.CharField("Title",max_length=200)
    publication_remarks = models.TextField("Remarks")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')

    def __str__(self):
        return self.release_no

    class Meta:
        verbose_name_plural = "Publications"
        ordering = ['priority_no']


