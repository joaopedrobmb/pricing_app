import uuid
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import ListView, FormView, DeleteView, DetailView
from django.shortcuts import get_object_or_404, redirect
from .models import QuotationRequests, Equipment
from .forms import QuotationRequestForm, EquipmentFormSet

class QuotationRequestsListView(ListView):
    model = QuotationRequests
    template_name = "quotation_requests/quotationrequests_list.html"

class QuotationRequestsCreateView(FormView):
    template_name = "quotation_requests/quotationrequests_form.html"
    form_class = QuotationRequestForm
    success_url = reverse_lazy("quotationrequests_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Gerar e armazenar o ID temporário na sessão, se não existir
        if "temp_id" not in self.request.session:
            self.request.session["temp_id"] = str(uuid.uuid4())
            self.request.session.modified = True

        context["temp_id"] = self.request.session["temp_id"]

        # Criar formset para os equipamentos
        context["formset"] = EquipmentFormSet(self.request.POST or None)
        return context

    def form_valid(self, form):
        temp_id = self.request.session.get("temp_id")

        if not temp_id:
            return self.form_invalid(form)

        # Criar o orçamento no banco de dados
        quotation_request = form.save()

        # Associar os equipamentos ao orçamento real e criar ID composto
        equipments = Equipment.objects.filter(temp_id=temp_id)
        for idx, equipment in enumerate(equipments, start=1):
            equipment.quotation_request = quotation_request
            equipment.composed_id = f"{quotation_request.id:04d}-{idx:02d}"
            equipment.temp_id = None
            equipment.save()

        # Remover o temp_id da sessão
        del self.request.session["temp_id"]
        self.request.session.modified = True

        return super().form_valid(form)

class QuotationRequestsUpdateView(FormView):
    template_name = "quotation_requests/quotationrequests_form.html"
    form_class = QuotationRequestForm
    success_url = reverse_lazy("quotationrequests_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quotation_request = get_object_or_404(QuotationRequests, pk=self.kwargs["pk"])

        context["form"] = QuotationRequestForm(instance=quotation_request)
        context["formset"] = EquipmentFormSet(self.request.POST or None, instance=quotation_request)
        return context

    def form_valid(self, form):
        quotation_request = get_object_or_404(QuotationRequests, pk=self.kwargs["pk"])

        # Salvar o formulário do orçamento
        form.instance = quotation_request
        form.save()

        # Atualizar os equipamentos associados ao orçamento
        equipments = Equipment.objects.filter(quotation_request=quotation_request)
        for idx, equipment in enumerate(equipments, start=1):
            equipment.composed_id = f"{quotation_request.id:04d}-{idx:02d}"
            equipment.save()

        return super().form_valid(form)

class QuotationRequestsDetailView(DetailView):
    model = QuotationRequests
    template_name = "quotation_requests/quotationrequests_detail.html"
    context_object_name = "quotation_request"

class QuotationRequestsDeleteView(DeleteView):
    model = QuotationRequests
    success_url = reverse_lazy("quotationrequests_list")

def add_equipment(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método não permitido."}, status=405)

    quotation_request_id = request.POST.get("quotation_request_id")

    if not quotation_request_id:
        return JsonResponse({"error": "Erro: ID não fornecido."}, status=400)

    try:
        uuid.UUID(quotation_request_id)  # Validar UUID
    except ValueError:
        return JsonResponse({"error": "Erro: ID inválido."}, status=400)

    # Obter dados do equipamento
    equipment_type = request.POST.get("equipment_set-0-equipment_type")
    equipment_model = request.POST.get("equipment_set-0-equipment_model")
    quantity = request.POST.get("equipment_set-0-quantity")
    price = request.POST.get("equipment_set-0-price") or None  # Tratar campo vazio

    # Criar e salvar o equipamento
    equipment = Equipment.objects.create(
        equipment_type=equipment_type,
        equipment_model=equipment_model,
        quantity=quantity,
        price=price,
        temp_id=quotation_request_id
    )

    return JsonResponse({
        "success": True,
        "equipment_id": equipment.id,
        "equipment_type": equipment_type,
        "equipment_model": equipment_model,
        "quantity": quantity,
        "price": price
    })

def cancel_quotation_request(request):
    if "temp_id" in request.session:
        temp_id = request.session["temp_id"]
        Equipment.objects.filter(temp_id=temp_id).delete()
        del request.session["temp_id"]
        request.session.modified = True

    return redirect("quotationrequests_list")
