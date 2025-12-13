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

# ==============================================================================
# FUNÇÃO AUXILIAR INTELIGENTE (O Segredo do Filtro)
# ==============================================================================
def get_dono_dos_dados(user):
    """
    Retorna quem é o 'dono' real dos dados que o usuário logado deve ver.
    - Se for OPERADOR: O dono é a 'empresa_pai' (o Gerente).
    - Se for GERENTE: O dono é ele mesmo.
    """
    if user.cargo == 'OPERADOR' and user.empresa_pai:
        return user.empresa_pai
    return user

# ==============================================================================
# VIEWSETS
# ==============================================================================

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    
    # Define permissões
    def get_permissions(self):
        # Permitimos criar conta (AllowAny) se for cadastro público,
        # ou você pode mudar para IsAuthenticated se só admin cria.
        if self.action == 'create':
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        
        # SuperAdmin vê todas as empresas
        if user.is_superuser or user.cargo == 'SUPERADMIN':
            return Empresa.objects.all()
        
        # Gerente/Operador vê apenas seus próprios dados de usuário
        return Empresa.objects.filter(pk=user.pk)


class EstoqueViewSet(viewsets.ModelViewSet):
    queryset = Estoque.objects.all()
    serializer_class = EstoqueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.cargo == 'SUPERADMIN':
            return Estoque.objects.all()
        
        dono = get_dono_dos_dados(user)
        return Estoque.objects.filter(empresa=dono)


class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.cargo == 'SUPERADMIN':
            return Veiculo.objects.all()
        
        dono = get_dono_dos_dados(user)
        return Veiculo.objects.filter(empresa=dono)


class PneuViewSet(viewsets.ModelViewSet):
    queryset = Pneu.objects.all()
    serializer_class = PneuSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.cargo == 'SUPERADMIN':
            return Pneu.objects.all()
        
        dono = get_dono_dos_dados(user)
        return Pneu.objects.filter(empresa=dono)


class MovimentacaoPneuViewSet(viewsets.ModelViewSet):
    queryset = MovimentacaoPneu.objects.all()
    serializer_class = MovimentacaoPneuSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.cargo == 'SUPERADMIN':
            return MovimentacaoPneu.objects.all()
        
        dono = get_dono_dos_dados(user)
        # Nota: Movimentação não tem campo 'empresa' direto, filtramos através do Pneu
        return MovimentacaoPneu.objects.filter(pneu__empresa=dono)


class ManutencaoViewSet(viewsets.ModelViewSet):
    queryset = Manutencao.objects.all()
    serializer_class = ManutencaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.cargo == 'SUPERADMIN':
            return Manutencao.objects.all()
        
        dono = get_dono_dos_dados(user)
        return Manutencao.objects.filter(pneu__empresa=dono)


class InspecaoViewSet(viewsets.ModelViewSet):
    queryset = Inspecao.objects.all()
    serializer_class = InspecaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.cargo == 'SUPERADMIN':
            return Inspecao.objects.all()
        
        dono = get_dono_dos_dados(user)
        return Inspecao.objects.filter(pneu__empresa=dono)