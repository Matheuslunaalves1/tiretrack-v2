from rest_framework import viewsets, permissions
from .models import (
    Empresa,

    Estoque,
    Veiculo,
    Pneu,
    MovimentacaoPneu,
    Manutencao,
    Inspecao,
)
from .serializers import (
    EmpresaSerializer,

    EstoqueSerializer,
    VeiculoSerializer,
    PneuSerializer,
    MovimentacaoPneuSerializer,
    ManutencaoSerializer,
    InspecaoSerializer,
)


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()





class EstoqueViewSet(viewsets.ModelViewSet):
    queryset = Estoque.objects.all()
    serializer_class = EstoqueSerializer
    permission_classes = [permissions.IsAuthenticated]


class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    permission_classes = [permissions.IsAuthenticated]


class PneuViewSet(viewsets.ModelViewSet):
    queryset = Pneu.objects.all()
    serializer_class = PneuSerializer
    permission_classes = [permissions.IsAuthenticated]


class MovimentacaoPneuViewSet(viewsets.ModelViewSet):
    queryset = MovimentacaoPneu.objects.all()
    serializer_class = MovimentacaoPneuSerializer
    permission_classes = [permissions.IsAuthenticated]


class ManutencaoViewSet(viewsets.ModelViewSet):
    queryset = Manutencao.objects.all()
    serializer_class = ManutencaoSerializer
    permission_classes = [permissions.IsAuthenticated]


class InspecaoViewSet(viewsets.ModelViewSet):
    queryset = Inspecao.objects.all()
    serializer_class = InspecaoSerializer
    permission_classes = [permissions.IsAuthenticated]
