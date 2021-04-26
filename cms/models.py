from django.db import models

# Create your models here.


class Category(models.Model):
    category = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category


class Product(models.Model):

    STATUS_CHOICES = (
        ('Available', 'item ready to be purchased'),
        ('sold', 'item sold'),
        ('restocking', 'item restocking in few days'))

    name = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.IntegerField(default=0, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Available', blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('OnTransit', 'OnTransit'),
        ('Delivered', 'Delivered')
    )

    customer = models.CharField(max_length=100, blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    issue_quantity = models.IntegerField(default=0, blank=True, null=True)
    date_created = models.DateTimeField(auto_now=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS, blank=True)
    note = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.customer )


class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL )
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def _str__(self):
        return self.product.name





