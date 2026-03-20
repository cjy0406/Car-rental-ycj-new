"""Main URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vendors/', include('vendors.urls')),
    path('customers/', include('customers.urls')),
    path('analytics/', include('analytics.urls')),
    path('', include('core.urls')),  # 首頁路由
    # 如果之後加 api，再加這一行：
    # path('api/', include('api.urls')),
    path('api/', include('api.urls')),
]

# 開發模式下提供媒體檔案（圖片等）
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)