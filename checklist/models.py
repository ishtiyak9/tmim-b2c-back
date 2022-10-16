from django.db import models
from user.models import User
# from category.models import Category

class Tasklist(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="tasklist_created_by",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        related_name="tasklist_updated_by",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tasklist'

class Checklist(models.Model):
    # category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True,verbose_name='checkcategory')
    tasklist = models.ForeignKey(Tasklist, on_delete=models.CASCADE, null=True, blank=True,verbose_name='tasklist')
    title = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    complete = models.IntegerField(blank=True, null=True)
    customer = models.ForeignKey(User, limit_choices_to={'user_type': "customer"}, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name="checklist_created_by",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        related_name="checklist_updated_by",
        on_delete=models.CASCADE
    )
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'checklist'