from django.contrib import admin
from restaurantManagement.models import Restaurant, RestaurantCategory, MenuSection, MenuItem, OpeningHours
from orderManagement.models import Order, OrderItem 
from userManagement.models import Address
from ratingManagement.models import Rating

###change sooon
#from restaurantManagement.views import RestaurantCategoryList, RestaurantList

#admin.site.register(Restaurant)
#admin.site.register(RestaurantCategory)
#admin.site.register(MenuSection)
#admin.site.register(MenuItem)
#admin.site.register(OpeningHours)

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(Rating)

class RestaurantCategoryAdminInline(admin.TabularInline):
    model=RestaurantCategory
   
    

    
    
class MenuItemAdminInline(admin.TabularInline):
    model=MenuItem
    fields=['name','description','price']
    
class OpeningHoursInline(admin.TabularInline):
    model=OpeningHours
    extra=1
    
    

class RestaurantAdmin(admin.ModelAdmin):
    
    exclude=[]
    inlines=[RestaurantCategoryAdminInline,OpeningHoursInline]
    
    def get_form(self, request, obj=None, **kwargs):
        current_user = request.user
        if not current_user.is_superuser:
            self.exclude = ('owner','name','street1','street2','postcode','city','country')
            
        form = super(RestaurantAdmin, self).get_form(request, obj, **kwargs)
        form.current_user = current_user
        return form

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        obj.save()
        
    def queryset(self, request):
        if request.user.is_superuser:
            return Restaurant.objects.all()
        return Restaurant.objects.filter(owner=request.user)

  
    
class RestaurantCategoryAdmin(admin.ModelAdmin):
    pass

class MenuSectionAdmin(admin.ModelAdmin):
    exclude=[]
   
    inlines=[MenuItemAdminInline]
    
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.restaurant.owner = request.user
        obj.save()
        
    def queryset(self, request):
        if request.user.is_superuser:
            return MenuSection.objects.all()
        return MenuSection.objects.filter(restaurant__owner=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "restaurant":
            kwargs["queryset"] = Restaurant.objects.filter(owner=request.user)
        return super(MenuSectionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
   

class MenuItemAdmin(admin.ModelAdmin):
    pass
  
class OpeningHoursAdmin(admin.ModelAdmin):
    pass


admin.site.register(Restaurant,RestaurantAdmin)
admin.site.register(MenuSection,MenuSectionAdmin)