from rest_framework import serializers
from .models import (
    Empresa,

    Estoque,
    Veiculo,
    Pneu,
    MovimentacaoPneu,
    Manutencao,
    Inspecao,
)


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ["id", "username", "email", "nome", "cnpj", "data_contrato", "status_assinatura"]





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
