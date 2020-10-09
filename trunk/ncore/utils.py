from django_oss_storage.backends import OssMediaStorage as DefaultOssMediaStorage
from django_oss_storage.backends import OssStaticStorage as DefaultOssStaticStorage
from django.conf import settings
from pathlib import Path
import time, random

class OssMediaStorage(DefaultOssMediaStorage):
    def url(self, name):
        key = self._get_key_name(name)
        url = getattr(settings, "OSS_PROXY_STATIC_URL")
        return url + key

    def _save(self, name, content):
        p = Path(name)
        # 定义文件名，年月日时分秒_随机数_原名.后缀
        fn = "{0}_{1}_{2}{3}".format(time.strftime('%Y%m%d%H%M%S'),
            random.randint(0,100), p.stem, p.suffix)
        # 重写合成文件名
        name = str(p.parent.joinpath(fn))
        return super(OssMediaStorage, self)._save(name, content)


class OssStaticStorage(DefaultOssStaticStorage):
    def url(self, name):
        key = self._get_key_name(name)
        url = getattr(settings, "OSS_PROXY_STATIC_URL")
        return url + key

    def _save(self, name, content):
        p = Path(name)
        # 定义文件名，年月日时分秒_随机数_原名.后缀
        fn = "{0}_{1}_{2}{3}".format(time.strftime('%Y%m%d%H%M%S'),
            random.randint(0,100), p.stem, p.suffix)
        # 重写合成文件名
        name = str(p.parent.joinpath(fn))
        return super(OssStaticStorage, self)._save(name, content)

