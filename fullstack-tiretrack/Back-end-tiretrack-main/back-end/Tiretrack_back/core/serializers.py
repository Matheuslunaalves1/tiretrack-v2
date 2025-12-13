from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import (
    Empresa,
    Estoque,
    Veiculo,
    Pneu,
    MovimentacaoPneu,
    Manutencao,
    Inspecao,
)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)

        data['user'] = {
            'id': self.user.id,
            'nome': self.user.nome_fantasia or self.user.username,
            'email': self.user.email,
            'cargo': self.user.cargo, 
            'permissao': self.user.cargo, 
            'tipoAcesso': 'Proprietaria' if self.user.cargo == 'SUPERADMIN' else 'Cliente'
        }
        return data

class EmpresaSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Empresa
        fields = [
            "id", "username", "email", "password", 
            "nome_fantasia", "cnpj", "cargo", "empresa_pai",
            "status_assinatura"
        ]

    def create(self, validated_data):
        
        empresa = Empresa(**validated_data)
        empresa.set_password(password)  
        empresa.save()
        return empresa


class EstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estoque
        fields = "__all__"


class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = "__all__"


class PneuSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Pneu
        fields = "__all__"


class MovimentacaoPneuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimentacaoPneu
        fields = "__all__"


class ManutencaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manutencao
        fields = "__all__"


class InspecaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inspecao
        fields = "__all__"