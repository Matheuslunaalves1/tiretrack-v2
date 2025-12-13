from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


# --------- Empresa (Custom User Model) ---------
class Empresa(AbstractUser):
    nome = models.CharField(max_length=60, unique=True) # Nome da empresa
    cnpj = models.CharField(max_length=18, unique=True, null=True, blank=True) # CNPJ
    data_contrato = models.DateField(null=True, blank=True)
    status_assinatura = models.BooleanField(default=True)
    
    # Campos de autenticação
    USERNAME_FIELD = 'username' # Usar o campo username herdado para login
    REQUIRED_FIELDS = ['email', 'nome']

    objects = UserManager()

# --------- Estoque ---------
class Estoque(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="estoques")
    nome = models.CharField(max_length=50)
    rua = models.CharField(max_length=45)
    bairro = models.CharField(max_length=45)
    cidade = models.CharField(max_length=45)
    uf = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.nome} - {self.empresa.nome}"


# --------- Veículo ---------
class Veiculo(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="veiculos")
    placa = models.CharField(max_length=10)
    modelo = models.CharField(max_length=45)
    quilometragem_atual = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)
    ano = models.SmallIntegerField()
    configuracao_eixo = models.CharField(max_length=15)

    def __str__(self):
        return self.placa



# --------- Pneu ---------
class Pneu(models.Model):
    STATUS_CHOICES = [
        ("ESTOQUE", "Estoque"),
        ("VEICULO", "Veículo"),
        ("MANUTENCAO", "Manutenção"),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="pneus")
    estoque = models.ForeignKey(Estoque, on_delete=models.SET_NULL, null=True, blank=True)    
    numero_fogo = models.CharField(max_length=20, unique=True)
    data_compra = models.DateField()
    valor_compra = models.DecimalField(max_digits=10, decimal_places=2)
    vida_atual = models.IntegerField()
    km_total_acumulado = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="ESTOQUE")

    def __str__(self):
        return self.numero_fogo


# --------- Movimentação de Pneu ---------
class MovimentacaoPneu(models.Model):
    TIPO_CHOICES = [
        ("ENTRADA", "Entrada"),
        ("INSTALACAO", "Instalação"),
        ("RETIRADA", "Retirada"),
        ("TRANSFERENCIA", "Transferência"),
        ("MANUTENCAO", "Manutenção"),
    ]

    pneu = models.ForeignKey(Pneu, on_delete=models.CASCADE)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.SET_NULL, null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    data_movimentacao = models.DateTimeField(auto_now_add=True)
    origem = models.CharField(max_length=50, blank=True)
    destino = models.CharField(max_length=50, blank=True)
    observacao = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tipo} - {self.pneu.numero_fogo}"


# --------- Manutenção ---------
class Manutencao(models.Model):
    pneu = models.ForeignKey(Pneu, on_delete=models.CASCADE)
    tipo_servico = models.CharField(max_length=45)
    data_servico = models.DateField()
    custo_servico = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.tipo_servico} - {self.pneu.numero_fogo}"


# --------- Inspeção ---------
class Inspecao(models.Model):
    pneu = models.ForeignKey(Pneu, on_delete=models.CASCADE, related_name="inspecoes")
    data_inspecao = models.DateField()
    hodometro_veiculo = models.DecimalField(max_digits=10, decimal_places=2)
    medicao_sulco = models.DecimalField(max_digits=4, decimal_places=1)
    pressao_psi = models.SmallIntegerField()
    observacao = models.CharField(max_length=255)

    def __str__(self):
        return f"Inspeção {self.data_inspecao} - {self.pneu.numero_fogo}"
