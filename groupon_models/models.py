# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from time import timezone

from django.db import models


class User(models.Model):
    firstname = models.CharField(max_length=200, verbose_name="Нэр")
    lastname = models.CharField(max_length=200, verbose_name="Овог")
    email = models.EmailField(verbose_name="И-мэйл хаяг")
    password = models.CharField(max_length=200, verbose_name="Нууц үг")
    following_orginisations = models.ManyToManyField('Organisation', verbose_name='Дагаж буй байгуулгууд', related_name='following')
    image = models.ImageField(verbose_name="Зураг",upload_to="user/images", default='user/images/avatar-placeholder.png')
    save_sale = models.ManyToManyField('Sale', verbose_name='Хадгалсан хямдрал')

    def __str__(self):
        return '%s' % self.email

    def __unicode__(self):
        return self.email

    class Meta:
        db_table = "user"
        verbose_name = "Хэрэглэгч"
        verbose_name_plural = "Хэрэглэгчид"


class Organisation(models.Model):
    name = models.CharField(max_length=200, verbose_name="Байгууллагын нэр")
    url = models.URLField(max_length=200, verbose_name="Веб Сайт")
    user = models.OneToOneField('User', verbose_name='Хэрэглэгч', null=True)
    cover = models.ImageField(verbose_name="Cover Зураг", upload_to='organisation/covers')
    profile_image = models.ImageField(verbose_name="Profile Зураг", upload_to='organisation/profile_pictures')
    description = models.TextField(verbose_name="Танилцуулга")

    def __str__(self):
        return '%s' % self.name

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "organisation"
        verbose_name = "Байгууллага"
        verbose_name_plural = "Байгууллагууд"


class Branch(models.Model):
    name= models.CharField(max_length=200,verbose_name="Салбарын нэр")
    phone_number = models.IntegerField(verbose_name="Утасны дугаар")
    address = models.CharField(max_length=200, verbose_name="Хаяг")
    location = models.CharField(max_length=200, verbose_name="Байрлал")
    description = models.CharField(max_length=200, verbose_name="Тайлбар", null=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    profile_image = models.ImageField(verbose_name="Салбарын profile зураг", upload_to="branch/profile_pictures")
    product = models.ManyToManyField('Product')
    cover = models.ImageField(verbose_name='Cover', upload_to='branch/cover', null=True)

    def __str__(self):
        return '%s' % self.name

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "branch"
        verbose_name = "Салбар"
        verbose_name_plural = "Салбарууд"


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Ангилалын нэр")
    image = models.ImageField(verbose_name='Ангилалын зураг', upload_to='category/images', null=True)

    def __str__(self):
        return '%s' % self.name

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "category"
        verbose_name = "Ангилал"
        verbose_name_plural = "Ангилалууд"


class SubCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name="Дэд ангилалын нэр")
    parent = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.name

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "subcategory"
        verbose_name = "Дэд ангилал"
        verbose_name_plural = "Дэд ангилалууд"


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Барааны нэр")
    price = models.CharField(max_length=200, verbose_name="Үнэ")
    details = models.TextField(verbose_name="Дэлгэрэнгүй")
    rating = models.IntegerField(verbose_name="Үнэлгээ")
    user = models.ForeignKey(User, on_delete=models.CASCADE) # ?
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="product/picture")

    def __str__(self):
        return '%s' % self.name

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "product"
        verbose_name = "Бараа"
        verbose_name_plural = "Бараанууд"


class Sale(models.Model):
    start_date = models.DateTimeField(verbose_name="Хямдрал эхэлсэн өдөр",)
    finish_date = models.DateTimeField(verbose_name="Хямдрал дуусах өдөр",)
    precent = models.FloatField(verbose_name="Хувь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    thumbnail = models.ImageField(verbose_name="Зураг", upload_to='sale/thumbnail')
    name = models.CharField(max_length=200,verbose_name='Нэр')
    avatar = models.ImageField(verbose_name='Avatar', upload_to='sale/avatar', default='user/images/avatar-placeholder.png')
    price = models.CharField(max_length=200,verbose_name='Үнэ')

    def __str__(self):
        return '%s' % self.name

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "sale"
        verbose_name = "Хямдрал"
        verbose_name_plural = "Хямдралууд"


class Question(models.Model):
    question = models.CharField(max_length=200, verbose_name="Асуулт")
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.question

    def __unicode__(self):
        return self.question

    class Meta:
        db_table = "question"
        verbose_name = "Асуулт"
        verbose_name_plural = "Асуултууд"


class Answer(models.Model):
    answer = models.CharField(max_length=200, verbose_name="Хариулт")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.answer

    def __unicode__(self):
        return self.answer

    class Meta:
        db_table = "answer"
        verbose_name = "Хариулт"
        verbose_name_plural = "Хариултууд"


class UserReview(models.Model):
    rating = models.CharField(max_length=200,verbose_name="Үнэлгээ")
    comment = models.CharField(max_length=200, verbose_name="Сэтгэгдэл")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.rating

    def __unicode__(self):
        return self.rating

    class Meta:
        db_table = "review"
        verbose_name = "Шүүмж"
        verbose_name_plural = "Шүүмжүүд"


