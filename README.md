# backend development framework

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Background
基于django2.2.X的后端最新的基础开发架构，对返回值进行了一层整体处理以适应前端开发需要，不再返回HTTP状态码，直接将错误码以json格式进行返回，500错误仍希望抛出，目的是为了让sentry捕获。

## Install
This project uses [python3.5+](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/). Go check them out if you don't have them locally installed.

$ pip install -r requirements.txt

## Usage
### third-app
* django_oss_storage: 阿里云oss存储插件
* rest_framework: rest开发插件
* django_filters: filter插件
* easyaudit: 日志插件
* drf_yasg: swagger文档插件
### self-app
* ncore: 核心开发组件（必选）
    * trunk/ncore/verify_image_code/ValidationCodeImageService 图像验证码功能
    * trunk/ncore/views/LoginView 账号密码session登录
    * trunk/ncore/serializers/custom_validation_error 序列化异常抛出函数
    * trunk/ncore/views/CustomObtainJSONWebToken 获取JWT证书
    * trunk/ncore/views/CustomRefreshJSONWebToken 刷新JWT证书
* dingtalkapi: 钉钉内部应用组件（可选）
    * trunk/dingtalkapi/services/AKCService 钉钉api服务
    * trunk/dingtalkapi/views/DingTalkLoginView 钉钉userid事先录入匹配session登录
* entwechatapi: 企业微信应用组件（可选）
    * trunk/entwechatapi/services/EWCService 企业微信api服务
    * trunk/entwechatapi/views/EntWeChatLoginView 企业微信userid事先录入匹配session登录
* wechatminiprogramapi: 微信小程序应用组件（可选）
    * trunk/wechatminiprogramapi/services/WMPCService 微信小程序api服务
    * trunk/wechatminiprogramapi/views/WeChatMiniProgramCodeView 微信小程序thirdsession
    * trunk/wechatminiprogramapi/views/WeChatMiniProgramLoginView 微信小程序自动账号session登录
* approvalflow: 审批流组件（可选）
    * trunk/approvalflow/services/ApprovalFlowService 审批流核心服务

### note
序列化中抛出异常易用custom_validation_error
生成po文件：python manage.py makemessages -l zh_Hans
生成mo文件：python manage.py compilemessages
jwt使用 http headers中加入Key:Authorization Value:Bearer realtoken
jwt中验证码数据可以使用键值对方式进行存储，前端生成随机数，后端保存等
ForeignKey：on_delete=models.PROTECT应用层逻辑
settings中AUTH_USER_MODEL = "ncore.User"，可自行调整扩展
python manage.py makemigrations --empty  重建migrate

## maintainers
[@Joe](mailto:zhaojiejoe@gmail.com)

## Contributing
Feel free to dive in!
### Contributors
This project exists thanks to all the people who contribute.

## License
[MIT](LICENSE) © Joe
