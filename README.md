### 现行版本

python: 3.10.14

Django: 5.0.3

### 使用方法

使用命令行进入`*`所标记文件夹中，执行`python manage.py runserver 8000`命令，成功后访问http://127.0.0.1:8000/main/flights

```
FlightTicketBooking *
├─FlightTicketBooking
│  └─__pycache__
└─main
    ├─migrations
    │  └─__pycache__
    ├─static
    │  └─css
    ├─templates
    └─__pycache__
```

注意：

若出现错误或`models.py`进行修改，则仍在该文件夹下执行`python manage.py makemigrations`， `python manage.py migrate` 命令

### 关于部署

该项目可用uWSGI部署，部署时注意`./FlightTicketBooking/settings.py`要进行更改，直接将`./FlightTicketBooking/settings_deploy.py`中的内容覆盖到原`settings.py`即可
