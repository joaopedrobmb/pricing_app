from django.db import models
import uuid

class QuotationRequests(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="Título do Projeto", max_length=150, null=False, blank=False)
    customer = models.CharField(verbose_name="Cliente", max_length=100, null=False, blank=False)
    SALE_STATES = [
        ("AC", "Acre"), ("AL", "Alagoas"), ("AP", "Amapá"), ("AM", "Amazonas"), ("BA", "Bahia"), ("CE", "Ceará"),
        ("DF", "Distrito Federal"), ("ES", "Espírito Santo"), ("GO", "Goiás"), ("MA", "Maranhão"), ("MT", "Mato Grosso"),
        ("MS", "Mato Grosso do Sul"), ("MG", "Minas Gerais"), ("PA", "Pará"), ("PB", "Paraíba"), ("PR", "Paraná"),
        ("PE", "Pernambuco"), ("PI", "Piauí"), ("RJ", "Rio de Janeiro"), ("RN", "Rio Grande do Norte"),
        ("RS", "Rio Grande do Sul"), ("RO", "Rondônia"), ("RR", "Roraima"), ("SC", "Santa Catarina"), ("SP", "São Paulo"),
        ("SE", "Sergipe"), ("TO", "Tocantins"),
    ]
    sale_state = models.CharField(verbose_name="Estado", max_length=2, choices=SALE_STATES, null=False, blank=False)
    difal_check = models.BooleanField(verbose_name="DIFAL?", default=False)
    review_count = models.IntegerField(verbose_name="Revisão da Solicitação", default=0)
    quotation_total_value = models.DecimalField(verbose_name="Valor Orçado", max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(verbose_name="Criada em", auto_now_add=True, null=False, blank=False)
    responded_on = models.DateTimeField(verbose_name="Orçado em", null=True, blank=True)
    deadline = models.DateTimeField(verbose_name="Deadline", null=False, blank=False)

    def revise_quotation(self):
        self.review_count += 1
        self.save()

    def mark_as_responded(self):
        from django.utils.timezone import now
        self.responded_at = now()
        self.save()

class Equipment(models.Model):
    quotation_request = models.ForeignKey(QuotationRequests, on_delete=models.CASCADE, null=True, blank=True)
    temp_id = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True)
    composed_id = models.CharField(max_length=255, blank=True, null=True)
    EQUIPMENT_TYPES = [
        ("TA", "Tanque Armazenagem"), ("TTE", "Tanque Tratamento de Efluentes"), ("VP", "Vaso de Pressão"),
    ]
    equipment_type = models.CharField(verbose_name="Tipo de Equipamento", max_length=30, choices=EQUIPMENT_TYPES, null=False, blank=False)
    EQUIPMENT_MODELS = [
        ("FPTE", "Fundo Plano/Tampo Elíptico"), ("FPTP", "Fundo Plano/Tampo Plano"), ("TH", "Tanque Horizontal"),
    ]
    equipment_model = models.CharField(verbose_name="Modelo de Equipamento", max_length=30, choices=EQUIPMENT_MODELS, null=False, blank=False)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)