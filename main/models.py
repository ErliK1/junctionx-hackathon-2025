from django.db import models

from django.contrib.auth.models import AbstractUser,Group
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user: User = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField("email address", unique=True)
    phone_number = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField()
    registered_date = models.DateField(auto_now_add=True)
    loyalty_points = models.IntegerField(default=0)
    role = models.ForeignKey(Group, related_name='users',
                             on_delete=models.CASCADE)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'birthday']

    objects = CustomUserManager()

    def __str__(self, ):
        return self.email


class Category(models.Model):
    class Meta:
        db_table = 'category'

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        db_table = 'product'

    name = models.CharField(max_length=100)
    base_price = models.IntegerField(default=0)
    is_customizable = models.BooleanField(default=False)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    product_type = models.ForeignKey('ProductType', related_name='products',
                                     on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='products',
                                 on_delete=models.CASCADE)
    stock_amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class ProductType(models.Model):
    class Meta:
        db_table = 'product_type'

    name = models.CharField(max_length=100)
    is_deliverable = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Option(models.Model):
    class Meta:
        db_table = 'option'

    name = models.CharField(max_length=100)
    base_price = models.IntegerField()
    product_type = models.ForeignKey(ProductType, related_name='options',
                                     on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class OrderOption(models.Model):
    class Meta:
        db_table = 'order_option'
        unique_together = ('order_item', 'option')

    option = models.ForeignKey(Option, related_name='order_options', on_delete=models.CASCADE)
    order_item = models.ForeignKey('OrderItem', related_name='order_options', on_delete=models.CASCADE)
    ammount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.option.name} {self.ammount}'


class ItemSize(models.Model):
    name = models.CharField(max_length=50)
    ammount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self, ):
        return self.name


class OrderItem(models.Model):
    class Meta:
        db_table = 'order_item'

    product = models.ForeignKey(Product, related_name='order_items',
                                on_delete=models.CASCADE)
    total_price = models.IntegerField()
    total_ammount = models.DecimalField(max_digits=10, decimal_places=2)
    item_size = models.ForeignKey(ItemSize, related_name='order_items',
                                  on_delete=models.CASCADE,
                                  null=True, blank=True)
    order = models.ForeignKey('Order', related_name='order_items',
                              on_delete=models.CASCADE)


class Address(models.Model):
    class Meta:
        db_table = 'address'

    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    building = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.IntegerField()


class Order(models.Model):
    class Meta:
        db_table = 'order'

    is_online = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField()
    address = models.ForeignKey(Address, related_name='orders', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, related_name='orders',
                             on_delete=models.CASCADE, null=True, blank=True)



class Giftcard(models.Model):
    class Meta:
        db_table = 'giftcard'

    from_user = models.ForeignKey(User, related_name='from_giftcards', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_giftcards', on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    total_ammount = models.IntegerField()
    current_amount = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)

