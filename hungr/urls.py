from django.conf.urls import patterns, include, url
from userManagement.views import UserList, UserDetail, AddressDetail, AddressList, RetrieveUserID, AddressCreater
from rest_framework.urlpatterns import format_suffix_patterns
from restaurantManagement.views import RatingList, CategoryCount, RestaurantList, RestaurantDetail, OpeningHoursDetail, RestaurantMenuDetail, MenuSectionDetail, MenuItemDetail, CategoryAbbreviationsList
from orderManagement.views import OrderDetail, OrderCreater, OrderItemCreater, OrderItemDetail, OrderUpdate
from ratingManagement.views import RatingCreate, RatingDetail
from django.contrib import admin

from home import views

admin.autodiscover()

urlpatterns = patterns('',
                       
    ###Browsable API login                   
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
         
    ###API
    url(r'^user-id/$', RetrieveUserID.as_view()),
    
    url(r'^user/$', UserList.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='user-detail'),
    url(r'^user/(?P<user>[0-9]+)/address/$', AddressList.as_view()),
    
    url(r'^address/$', AddressCreater.as_view()),
    url(r'^address/(?P<pk>[0-9]+)/$', AddressDetail.as_view(), name='address-detail'),
    
    url(r'^restaurant/$', RestaurantList.as_view()),
    url(r'^restaurant/(?P<pk>[0-9]+)/$', RestaurantDetail.as_view(), name='restaurant-detail'),
    
    url(r'^restaurant-orders/$', OrderUpdate.as_view()),
    
    url(r'^restaurant/(?P<pk>[0-9]+)/menu/$', RestaurantMenuDetail.as_view()),
    url(r'^restaurant/(?P<pk>[0-9]+)/opening-hours/$', OpeningHoursDetail.as_view(), name='opening_hours-detail'),
    url(r'^restaurant/(?P<restaurant>[0-9]+)/ratings/$', RatingList.as_view(), name='opening_hours-detail'),
    
    url(r'^order/$', OrderCreater.as_view()),
    url(r'^order/(?P<pk>[0-9]+)/$', OrderDetail.as_view(), name='order-detail'),
    
    url(r'^order-item/$', OrderItemCreater.as_view()),
    url(r'^order-item/(?P<pk>[0-9]+)/$', OrderItemDetail.as_view(), name='orderitem-detail'),

    url(r'^menu/(?P<pk>[0-9]+)/$', MenuSectionDetail.as_view(), name='menusection-detail'),
    url(r'^menu-item/(?P<pk>[0-9]+)/$', MenuItemDetail.as_view(), name='menuitem-detail'),

    url(r'^category/$', CategoryCount.as_view()),
    url(r'^category-help/$', CategoryAbbreviationsList.as_view()),

    url(r'^rating/$', RatingCreate.as_view()),
    url(r'^rating/(?P<pk>[0-9]+)/$', RatingDetail.as_view(), name='rating-detail'),
    
    ##################
    ###Auth Token
    ##################
    
    url(r'^auth-token/', 'rest_framework.authtoken.views.obtain_auth_token'),
    
    ##################
    ###Admin
    ##################
    
    url(r'^admin/', include(admin.site.urls)),
    
    ##################
    ###Home
    ##################
    
    url(r'^home/$', views.index, name='index'),
    url(r'^jquery/$', views.jquery, name='jquery'),
    
    ##################
    ###Dashboard
    ##################
    
    url(r'^$', 'userManagement.views.login_user'),
    
    url(r'^login/$', 'userManagement.views.login_user'),
    
    url(r'^logout/$', 'userManagement.views.logout_user'),
    
    url(r'^dashboard/$', 'restaurantManagement.views.show_dashboard'),
    
    url(r'^dashboard/restaurant$', 'restaurantManagement.views.show_restaurantInfo'),
    
    url(r'^dashboard/sections$', 'restaurantManagement.views.show_menuSections'),
    
    url(r'^dashboard/items$', 'restaurantManagement.views.show_menuItems'),
    
    url(r'^dashboard/order-history$', 'orderManagement.views.show_order_history'),
    
    url(r'^dashboard/ongoing-orders$', 'orderManagement.views.show_ongoing_orders'),
    
    url(r'^dashboard/order_notifications$', 'orderManagement.views.show_order_notification_panel'),
    
    url(r'^dashboard/order-details/(?P<order_id>[0-9]+)$', 'orderManagement.views.show_order_details'),
    
    url(r'^dashboard/order-details/(?P<order_id>[0-9]+)/accept$', 'orderManagement.views.accept_order'),
    
    url(r'^dashboard/order-details/(?P<order_id>[0-9]+)/reject$', 'orderManagement.views.reject_order'),
       
)

urlpatterns = format_suffix_patterns(urlpatterns)
