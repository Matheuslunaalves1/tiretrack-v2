from rest_framework import routers
from .views import (
    EmpresaViewSet,

    EstoqueViewSet,
    VeiculoViewSet,
    PneuViewSet,
    MovimentacaoPneuViewSet,
    ManutencaoViewSet,
    InspecaoViewSet,
)

router = routers.DefaultRouter()
router.register(r"empresas", EmpresaViewSet)

router.register(r"estoques", EstoqueViewSet)
router.register(r"veiculos", VeiculoViewSet)
router.register(r"pneus", PneuViewSet)
router.register(r"movimentacoes", MovimentacaoPneuViewSet)
router.register(r"manutencoes", ManutencaoViewSet)
router.register(r"inspecoes", InspecaoViewSet)

urlpatterns = router.urls
