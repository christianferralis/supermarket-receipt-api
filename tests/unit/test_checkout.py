"""Tests unitaires de départ pour les calculs de sous-total et de réduction."""

import pytest

from supermarket_receipt_api.checkout import (
    line_subtotal_cents,
    percentage_discount_cents,
    validate_quantity,
    three_for_two_discount_cents
)


@pytest.mark.parametrize(
    "unit_price_cents, quantity, unit, expected",
    [(100, 2, "piece", 200), (199, 1000, "gram", 199), (199, 2000, "gram", 398)],
)
def test_line_subtotal_nominal(
    unit_price_cents: int, quantity: int, unit: str, expected: int
) -> None:
    """Vérifier des calculs de sous-total.

    Aucun effet de bord ni application HTTP.

    Args:
        unit_price_cents (int): Prix unitaire en centimes fourni par pytest.
        quantity (int): Quantité de pièces ou de grammes fournie par pytest.
        unit (str): Unité de vente du cas paramétré.
        expected (int): Montant brut attendu en centimes.

    Returns:
        None: Le test réussit si le montant calculé correspond à l'attendu.

    Raises:
        AssertionError: Si le montant calculé diffère de expected.
    """
    assert line_subtotal_cents(unit_price_cents, quantity, unit) == expected


@pytest.mark.parametrize(
    "subtotal_cents, discount_percent, expected",
    [(1000, 20, 200), (1200, 10, 120), (800, 25, 200)]
    + [(100 * amount_euros, 10, 10 * amount_euros) for amount_euros in range(20, 114)],
)
def test_percentage_discount_nominal(
    subtotal_cents: int, discount_percent: int, expected: int
) -> None:
    """Vérifier des calculs de réduction en pourcentage.

    Aucun effet de bord ni application HTTP.

    Args:
        subtotal_cents (int): Montant brut en centimes fourni par pytest.
        discount_percent (int): Pourcentage de réduction fourni par pytest.
        expected (int): Réduction attendue en centimes.

    Returns:
        None: Le test réussit si la réduction calculée correspond à l'attendu.

    Raises:
        AssertionError: Si la réduction calculée diffère de expected.
    """
    assert percentage_discount_cents(subtotal_cents, discount_percent) == expected


@pytest.mark.parametrize("quantity, expected", [(1, 1), (3, 3)])
def test_validate_quantity(quantity: int, expected: int) -> None:
    """Vérifier la validation de la quantité.

    Args:
        quantity (int): Quantité à valider fournie par pytest.
        expected (int): Quantité attendue fournie par pytest.

    Returns:
        None: Le test réussit si la validation fonctionne correctement.

    Raises:
        AssertionError: Si la validation échoue pour des quantités valides.
    """
    # Cas valides
    assert validate_quantity(quantity) == expected


@pytest.mark.parametrize("quantity", [0, -1])
def test_validate_quantity_invalid(quantity: int) -> None:
    """Vérifier la validation de la quantité pour des cas invalides.

    Args:
        quantity (int): Quantité à valider fournie par pytest.

    Returns:
        None: Le test réussit si la validation échoue pour des quantités invalides.

    Raises:
        AssertionError: Si la validation réussit pour des quantités invalides.
    """
    # Cas invalides
    with pytest.raises(ValueError):
        validate_quantity(quantity)


@pytest.mark.parametrize("quantity", [1.5, "2", True])
def test_validate_quantity_invalid_types(quantity: float | str | bool) -> None:
    """Vérifier la validation de la quantité pour des types invalides.

    Args:
        quantity (float, str, bool): Quantité à valider fournie par pytest.

    Returns:
        None: Le test réussit si la validation échoue pour des types invalides.

    Raises:
        AssertionError: Si la validation réussit pour des types invalides.
    """
    # Cas invalides de type
    with pytest.raises(TypeError):
        validate_quantity(quantity)


@pytest.mark.parametrize(
    "quantity, unit_price_cents, expected",
    [
        (3, 100, 100),
        (4, 100, 100),
        (5, 100, 100),
        (6, 100, 200),
        (1, 100, 0),
        (2, 100, 0),
    ]
)
def test_three_for_two_discount_nominal(unit_price_cents: int, quantity: int, expected: int) -> None:
    """Vérifier le calcul de la réduction "3 pour 2".

    Aucun effet de bord ni application HTTP.

    Returns:
        None: Le test réussit si la réduction calculée correspond à l'attendu.

    Raises:
        AssertionError: Si la réduction calculée diffère de l'attendu.
    """
    assert three_for_two_discount_cents(unit_price_cents, quantity) == expected


