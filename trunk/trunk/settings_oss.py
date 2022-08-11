# OSS authentication settings
BUCKET_ACL_TYPE = "private"

# OSS File Storage Settings
OSS_BUCKET_NAME = "polarwin"

# Refer https://www.alibabacloud.com/help/zh/doc-detail/31837.htm about endpoint
OSS_ENDPOINT = "http://oss-cn-huhehaote.aliyuncs.com"

# use the actual url
OSS_PROXY_STATIC_URL = "http://oss.polarwin.cn/"

DEFAULT_FILE_STORAGE = 'ncore.utils.OssMediaStorage'
STATICFILES_STORAGE = 'ncore.utils.OssStaticStorage'

OSS_PREFIX = 'oss://'
# 这里的格式为 项目名/media
MEDIA_PREFIX = 'test/media/'
MEDIA_URL = '/test/media/'
ADMIN_MEDIA_PREFIX = '/test/static/admin'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_PREFIX = 'test/static/'
STATIC_URL = '/test/static/'

# Additional locations of static files
STATICFILES_DIRS = [
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #os.path.join(BASE_DIR, "static"),
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)