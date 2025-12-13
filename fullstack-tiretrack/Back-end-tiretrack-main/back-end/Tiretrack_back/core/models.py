from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class Empresa(AbstractUser):
    CARGO_CHOICES = (
        ('SUPERADMIN', 'Super Admin (Proprietária)'), 
        ('GERENTE', 'Gerente (Cliente Admin)'),       
        ('OPERADOR', 'Operador (Funcionário)'),       
    )

    nome_fantasia = models.CharField(max_length=60, verbose_name="Nome da Empresa")
    cnpj = models.CharField(max_length=18, unique=True, null=True, blank=True)
    status_assinatura = models.BooleanField(default=True)
    
    empresa_pai = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='funcionarios')
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES, default='SUPERADMIN')

    objects = UserManager()

    def __str__(self):
        return f"{self.username} - {self.get_cargo_display()}"


class Estoque(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="estoques")
    nome = models.CharField(max_length=50)
    localizacao = models.CharField(max_length=100, blank=True) 

    def __str__(self):
        return self.nome

class Veiculo(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="veiculos")
    placa = models.CharField(max_length=10)
    modelo = models.CharField(max_length=45)
    tipo = models.CharField(max_length=20, choices=[('CAMINHAO', 'Caminhão'), ('CARRETA', 'Carreta'), ('ONIBUS', 'Ônibus')], default='CAMINHAO')
    km_atual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    eixos = models.IntegerField(default=2)

    def __str__(self):
        return f"{self.placa} - {self.modelo}"

class Pneu(models.Model):
    STATUS_CHOICES = [
        ("ESTOQUE", "Em Estoque"),
        ("EM_USO", "Rodando no Veículo"),
        ("MANUTENCAO", "Em Manutenção"),
        ("SUCATA", "Descartado"),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="pneus")
    numero_fogo = models.CharField(max_length=20, unique=True)
    marca = models.CharField(max_length=50, null=True)
    modelo = models.CharField(max_length=50, null=True)
    medida = models.CharField(max_length=50, null=True)
    
    veiculo_atual = models.ForeignKey(Veiculo, on_delete=models.SET_NULL, null=True, blank=True, related_name='pneus_instalados')
    estoque_atual = models.ForeignKey(Estoque, on_delete=models.SET_NULL, null=True, blank=True)
    posicao_veiculo = models.CharField(max_length=10, null=True, blank=True)
    
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="ESTOQUE")
    km_total_acumulado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sulco_novo_mm = models.DecimalField(max_digits=4, decimal_places=1, default=18.0)

    def __str__(self):
        return f"Fogo: {self.numero_fogo} ({self.status})"


class MovimentacaoPneu(models.Model):
    TIPO_CHOICES = [
        ("MONTAGEM", "Montar no Veículo"),
        ("DESMONTAGEM", "Retirar do Veículo"),
        ("COMPRA", "Entrada por Compra"),
        ("DESCARTE", "Saída para Sucata"),
    ]

    pneu = models.ForeignKey(Pneu, on_delete=models.CASCADE)
    data_movimentacao = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    origem = models.CharField(max_length=50, blank=True)
    destino = models.CharField(max_length=50, blank=True)
    km_momento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observacao = models.TextField(blank=True)
    responsavel = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.tipo} - {self.pneu.numero_fogo}"



class Manutencao(models.Model):
    pneu = models.ForeignKey(Pneu, on_delete=models.CASCADE, related_name="manutencoes")
    tipo_servico = models.CharField(max_length=45)
    data_envio = models.DateField() # Data que foi para recapagem
    data_retorno = models.DateField(null=True, blank=True)
    custo = models.DecimalField(max_digits=10, decimal_places=2)
    km_no_envio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    concluido = models.BooleanField(default=False)
    descricao = models.CharField(max_length=255, blank=True)
    
    
    responsavel = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.tipo_servico} - {self.pneu.numero_fogo}"


class Inspecao(models.Model):
    pneu = models.ForeignKey(Pneu, on_delete=models.CASCADE, related_name="inspecoes")
    data_inspecao = models.DateTimeField(auto_now_add=True)
    pressao_psi = models.IntegerField()
    sulco_atual_mm = models.DecimalField(max_digits=4, decimal_places=1)
    alerta_critico = models.BooleanField(default=False)
    observacao = models.CharField(max_length=255, blank=True)
    responsavel = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Inspeção {self.data_inspecao} - {self.pneu.numero_fogo}"