from django.urls import path
from .views import home
from .views import base
from .views import password
from .views import index
from .views import index1
from .views import qr
from .views import about
from .views import service
from .views import contact
from .views import pages
from .views import cyber
from .views import cyber1
from .views import cyber2
from .views import cyber2b
from .views import cyber2c
from .views import cyber2d
from .views import privacy
from .views import privacy1
from .views import privacy2
from .views import privacy3
from .views import privacy4
from .views import privacy5
from .views import privacy6
from .views import privacy7
from .views import privacy8
from .views import privacy9
# from .views import message

urlpatterns = [
    path("", home, name="home"),
    path("base.html", base, name="base"),
    path("password.html", password, name="password"),
    path("index.html", index, name="index"),
    path("index1.html", index1, name="index1"),
    path("qr.html", qr, name="qr"),
    path("about.html", about, name="about"),
    path("service.html", service, name="service"),
    path("contact.html", contact, name="contact"),
    path("pages.html", pages, name="pages"),
    path("cyber.html", cyber, name="cyber"),
    path("cyber1.html", cyber1, name="cyber1"),
    path("cyber2.html", cyber2, name="cyber2"),
    path("cyber2b.html", cyber2b, name="cyber2b"),
    path("cyber2c.html", cyber2c, name="cyber2c"),
    path("cyber2d.html", cyber2d, name="cyber2d"),
    path("privacy.html", privacy, name="privacy"),
    path("privacy1.html", privacy1, name="privacy1"),
    path("privacy2.html", privacy2, name="privacy2"),
    path("privacy3.html", privacy3, name="privacy3"),
    path("privacy4.html", privacy4, name="privacy4"),
    path("privacy5.html", privacy5, name="privacy5"),
    path("privacy6.html", privacy6, name="privacy6"),
    path("privacy7.html", privacy7, name="privacy7"),
    path("privacy8.html", privacy8, name="privacy8"),
    path("privacy9.html", privacy9, name="privacy9"),
    # path("message.php", message, name="message"),
]