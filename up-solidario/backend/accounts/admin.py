from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Criamos uma classe de admin personalizada para o nosso User
class CustomUserAdmin(UserAdmin):
    # Adicionamos o nosso campo 'type' para que ele apareça no painel
    fieldsets = UserAdmin.fieldsets + (
        ('Tipos de Utilizador', {'fields': ('type',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Tipos de Utilizador', {'fields': ('type',)}),
    )

# Registamos o nosso modelo User com a configuração personalizada
admin.site.register(User, CustomUserAdmin)