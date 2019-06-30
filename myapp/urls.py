from django.conf.urls import url
from django.urls import path
from rest_framework import routers
from myapp.views import BooksViewSet,books_list,books_detail,books_patch_delete,books_load
from rest_framework_swagger.views import get_swagger_view
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()
router.register(r'books', BooksViewSet)
# router.register(r'clicks', ClicksViewSet)

schema_view = get_swagger_view(title='Books API')


urlpatterns = [
    url(r'^v1/books_load', books_load),
    url(r'^v1/books', books_list),
    url(r'^v1/books/<int:pk>', books_patch_delete),
    url(r'^external_books/<int:pk>', books_detail),
    url(r'^docs/', schema_view),
]

urlpatterns = format_suffix_patterns(urlpatterns)