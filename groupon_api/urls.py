
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/user', include('user_register.urls')),
    url(r'^api/organisation', include('organisation.urls')),
    url(r'^api/sale', include('sale.urls')),
    url(r'^api/product', include('product.urls')),
    url(r'^api/category', include('category.urls')),
    url(r'^api/subcategory', include('subcategory.urls')),
    url(r'^api/branch', include('branch.urls')),
    url(r'^api/review', include('user_review.urls')),
    url(r'^api/question', include('question.urls')),
    url(r'^api/answer', include('answer.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
