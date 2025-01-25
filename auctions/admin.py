from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.

class listingstAdmin(admin.ModelAdmin):
    list_display = ("user","title","description","bid","category" ,"image")
    list_filter = ("category",)
    


class categoryAdmin(admin.ModelAdmin):
    list_display = ("id","name")

admin.site.register(listings, listingstAdmin)
admin.site.register(category, categoryAdmin) 
admin.site.register(User)
admin.site.register(comments)
admin.site.register(bids)