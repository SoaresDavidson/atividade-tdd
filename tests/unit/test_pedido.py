import pytest
from unittest.mock import MagicMock
from pedido.pedido import Item, Pedido, contar_frete_gratis


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


def test_contar_frete_gratis_lista_vazia_retorna_zero():
    assert contar_frete_gratis([]) == 0


def test_contar_frete_gratis_todos_com_frete_gratis(pedido_grande):
    # pedido_grande: 2 x 22,00 + 2 x 7,00 + 1 x 15,00 = 73,00
    # outro: 50,00, exatamente no limite
    outro = Pedido("Carlos", [Item("Combo", 50.0, 1)])
    assert contar_frete_gratis([pedido_grande, outro]) == 2


def test_contar_frete_gratis_nenhum_com_frete_gratis(pedido_pequeno):
    # pedido_pequeno: 1 x 6,00 + 2 x 4,50 = 15,00
    # outro: 49,99, um centavo abaixo do limite
    outro = Pedido("Carlos", [Item("Combo", 49.99, 1)])
    assert contar_frete_gratis([pedido_pequeno, outro]) == 0


def test_contar_frete_gratis_lista_mista(pedido_pequeno, pedido_grande):
    # pedido_pequeno: 15,00 (sem frete grátis)
    # pedido_grande: 73,00 (com frete grátis)
    assert contar_frete_gratis([pedido_pequeno, pedido_grande]) == 1


# Requisito 2 — situacao(unidades_indisponiveis) -> str
# Escreva os testes ANTES de implementar o método


def test_situacao_tudo_disponivel_abaixo_de_50_confirmado(pedido_pequeno):
    # pedido_pequeno: subtotal 15,00, nenhuma unidade indisponível
    assert pedido_pequeno.situacao(0) == "Confirmado"


def test_situacao_tudo_disponivel_a_partir_de_50_confirmado_com_frete(pedido_grande):
    # pedido_grande: subtotal 73,00, nenhuma unidade indisponível
    assert pedido_grande.situacao(0) == "Confirmado com frete grátis"


def test_situacao_mais_de_25_por_cento_indisponivel_cancela_mesmo_com_frete(
    pedido_grande,
):
    # pedido_grande: 5 unidades, subtotal 73,00; 2 indisponíveis = 40%
    assert pedido_grande.situacao(2) == "Cancelado por falta de estoque"


def test_situacao_exatamente_25_por_cento_segue_para_o_frete():
    # 4 unidades, subtotal 80,00; 1 indisponível = exatamente 25%, não cancela
    pedido = Pedido("Carlos", [Item("X-burguer", 20.0, 4)])
    assert pedido.situacao(1) == "Confirmado com frete grátis"


def test_situacao_pouco_acima_de_25_por_cento_cancela():
    # 100 unidades; 26 indisponíveis = 26%
    pedido = Pedido("Carlos", [Item("Coxinha", 1.0, 100)])
    assert pedido.situacao(26) == "Cancelado por falta de estoque"


# Requisito 3 — sugerir_frete_gratis(sms_service) -> None
# Use MagicMock para simular o serviço de SMS
# Escreva os testes ANTES de implementar o método
def test_sugerir_frete_gratits(pedido_pequeno):
    sms_service_mock = MagicMock()
    pedido_pequeno.sugerir_frete_gratis(sms_service_mock)
    sms_service_mock.enviar.assert_called_once_with("Bruno", 15.0)
