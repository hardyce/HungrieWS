from django.conf.urls import patterns, include, url
from userManagement.views import UserList, UserDetail
from rest_framework.urlpatterns import format_suffix_patterns
from restaurantManagement.views import RestaurantList, RestaurantDetail, RestaurantCategoryList, RestaurantCategoryDetail, OpeningHoursDetail, RestaurantMenuDetail, MenuSectionDetail, MenuItemDetail
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^user/$', UserList.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='user-detail'),
    
    url(r'^restaurant/$', RestaurantList.as_view()),
    
    #url(r'^restaurant?lat=(?P<lat>[\d\.\-]*)$', RestaurantList.as_view()),
    
    url(r'^restaurant/(?P<pk>[0-9]+)/$', RestaurantDetail.as_view(), name='restaurant-detail'),
    
    url(r'^restaurant/(?P<pk>[0-9]+)/menu/$', RestaurantMenuDetail.as_view()),
    url(r'^restaurant/(?P<pk>[0-9]+)/opening-hours/$', OpeningHoursDetail.as_view(), name='opening_hours-detail'),
    
    
   
    url(r'^menu/(?P<pk>[0-9]+)/$', MenuSectionDetail.as_view(), name='menu'),
    #url(r'^menu/(?P<pk>[0-9]+)/$', Menu_Item.as_view()),

    
    url(r'^category/$', RestaurantCategoryList.as_view()),
    url(r'^category/(?P<pk>[0-9]+)/$', RestaurantCategoryDetail.as_view(), name='category-detail'),
    
   # url(r'^category/(?P<pk>[0-9]+)/$', CategoryDetail.as_view(), name='category-detail'),
    
    url(r'^auth-token/', 'rest_framework.authtoken.views.obtain_auth_token'),

    # Examples:
    # url(r'^$', 'hungr.views.home', name='home'),
    # url(r'^hungr/', include('hungr.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # requests to root serve login page
    url(r'^$', 'userManagement.views.login_user'),
    
    url(r'^login/$', 'userManagement.views.login_user'),
    
    url(r'^logout/$', 'userManagement.views.logout_user'),
    
    url(r'^dashboard/$', 'restaurantManagement.views.show_dashboard'),
    
    url(r'^dashboard/restaurant$', 'restaurantManagement.views.show_restaurantInfo'),
    
    url(r'^dashboard/sections$', 'restaurantManagement.views.show_menuSections'),
    
    url(r'^dashboard/items$', 'restaurantManagement.views.show_menuItems'),
    
)

urlpatterns = format_suffix_patterns(urlpatterns)
