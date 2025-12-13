from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Empresa, 
    Estoque, 
    Veiculo, 
    Pneu, 
    MovimentacaoPneu, 
    Manutencao, 
    Inspecao
)

# Configuração personalizada para o Usuário (Empresa)
class EmpresaAdmin(UserAdmin):
    model = Empresa
    
    # Colunas que aparecem na lista
    list_display = ['username', 'email', 'cargo', 'empresa_pai', 'nome_fantasia', 'is_active']
    
    # Filtros laterais
    list_filter = ['cargo', 'is_active', 'is_superuser']
    
    # Adicionando os nossos campos personalizados no formulário de edição
    fieldsets = UserAdmin.fieldsets + (
        ('Dados da Empresa/Cargo', {
            'fields': ('nome_fantasia', 'cnpj', 'cargo', 'empresa_pai', 'status_assinatura')
        }),
    )
    
    # Permite adicionar esses campos na criação também
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Dados da Empresa/Cargo', {
            'fields': ('email', 'nome_fantasia', 'cnpj', 'cargo', 'empresa_pai')
        }),
    )

# Registrando as tabelas para aparecerem no painel
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Estoque)
admin.site.register(Veiculo)
admin.site.register(Pneu)
admin.site.register(MovimentacaoPneu)
admin.site.register(Manutencao)
admin.site.register(Inspecao)