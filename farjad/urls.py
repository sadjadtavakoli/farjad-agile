"""farjad URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls.conf import include, path

from farjad.views.home import HomeView
from loan.views.loan_views import CreateLoanRequestAPIView

api_urlpatterns = ([
                       path(r'create-loan/', CreateLoanRequestAPIView.as_view(),
                            name="create-loan")

                   ], 'api')
urlpatterns = [

    path(r'admin/', admin.site.urls, name='admin'),
    path(r'api/', include(api_urlpatterns)),
    path(r'', HomeView.as_view(), name="home"),
    path(r'a', HomeView.as_view(), name="n-home"),
    path(r'', include('members.urls', namespace="members")),
    path(r'books/', include('books.urls', namespace="books")),

]
