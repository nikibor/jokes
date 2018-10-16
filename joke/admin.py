from django.contrib import admin

from joke.models import User, Joke, Log


class UserAdmin(admin.ModelAdmin):
    list_display = [
        'address',
    ]


class JokeAdmin(admin.ModelAdmin):
    list_display = [
        'text',
        'user',
    ]
    list_filter = ['user']


class LogAdmin(admin.ModelAdmin):
    list_display = [
        'request_time',
        'user',
        'user_address'
    ]
    list_filter = ['user']


admin.site.register(User, UserAdmin)
admin.site.register(Joke, JokeAdmin)
admin.site.register(Log, LogAdmin)
