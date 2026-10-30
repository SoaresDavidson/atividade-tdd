import pytest
from unittest.mock import MagicMock
from pedido.pedido import Item, Pedido


# =============================================================
# EXEMPLO — um teste pronto, para você copiar o formato
# =============================================================

def test_exemplo_quantidade_total(pedido_pequeno):
    # 1 café + 2 pães de queijo = 3 unidades
    assert pedido_pequeno.quantidade_total() == 3


# =============================================================
# PARTE 1 — Encontre os bugs
# Escreva um teste para cada bug. Cada teste deve FALHAR
# no código original. Não altere src/pedido/pedido.py ainda.
# =============================================================


def test_subtotal_multiplica_preco_pela_quantidade(pedido_pequeno):
    # 1 x 6,00 + 2 x 4,50 = 15,00
    assert pedido_pequeno.subtotal() == 15.0


def test_frete_gratis_com_subtotal_exatamente_50():
    # 30,00 + 20,00 = 50,00, que já dá direito a frete grátis
    pedido = Pedido("Carlos", [Item("Produto A", 30.0, 1), Item("Produto B", 20.0, 1)])
    assert pedido.tem_frete_gratis() is True


def test_item_mais_barato_retorna_menor_preco(pedido_pequeno):
    # Café 6,00 x Pão de queijo 4,50: o mais barato é o pão de queijo
    assert pedido_pequeno.item_mais_barato().nome == "Pão de queijo"


def test_total_com_desconto_subtrai_o_percentual():
    # 100,00 com 10% de desconto = 90,00
    pedido = Pedido("Carla", [Item("Combo", 100.0, 1)])
    assert pedido.total_com_desconto(10) == 90.0


# =============================================================
# PARTE 2 — Implemente com TDD
# Siga o ciclo: 🔴 escreva o teste → 🟢 implemente → 🟡 refatore
# =============================================================

# Requisito 1 — contar_frete_gratis(pedidos) -> int
# Escreva os testes ANTES de implementar a função



# Requisito 2 — situacao(unidades_indisponiveis) -> str
# Escreva os testes ANTES de implementar o método



# Requisito 3 — sugerir_frete_gratis(sms_service) -> None
# Use MagicMock para simular o serviço de SMS
# Escreva os testes ANTES de implementar o método
