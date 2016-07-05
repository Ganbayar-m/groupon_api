from django.contrib import admin
from groupon_models.models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Organisation)
admin.site.register(Branch)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserReview)


