from fastapi.testclient import TestClient

from supermarket_receipt_api.main import app

client = TestClient(app)


def test_checkout_panier_avec_promotion() -> None:
    """Vérifier le ticket complet d'un panier avec la promotion 3 pour 2.

    Returns:
        None: Le test réussit si le statut et le ticket correspondent au contrat.

    Raises:
        AssertionError: Si le statut ou le ticket diffère de l'attendu.
    """
    response = client.post(
        "/checkout", json={"items": [{"product_id": "toothbrush", "quantity": 3}]}
    )

    assert response.status_code == 200
    assert response.json() == {
        "lines": [
            {
                "product_id": "toothbrush",
                "name": "Brosse à dents",
                "quantity": 3,
                "unit": "piece",
                "unit_price_cents": 99,
                "subtotal_cents": 297,
                "discount_cents": 99,
                "total_cents": 198,
            }
        ],
        "subtotal_cents": 297,
        "discount_cents": 99,
        "total_cents": 198,
    }


def test_checkout_champ_manquant() -> None:
    """Vérifier qu'un article sans champ obligatoire est refusé.

    Returns:
        None: Le test réussit si l'API refuse la requête avec un détail d'erreur.

    Raises:
        AssertionError: Si le statut ou le corps de réponse diffère du contrat.
    """
    response = client.post("/checkout", json={"items": [{"quantity": 3}]})

    assert response.status_code == 422
    assert "detail" in response.json()


def test_checkout_champ_en_trop() -> None:
    """Vérifier qu'un article avec un champ supplémentaire est refusé.

    Returns:
        None: Le test réussit si l'API refuse la requête avec un détail d'erreur.

    Raises:
        AssertionError: Si le statut ou le corps de réponse diffère du contrat.
    """
    response = client.post(
        "/checkout",
        json={"items": [{"product_id": "toothbrush", "quantity": 3, "unit_price_cents": 1}]},
    )

    assert response.status_code == 422
    assert "detail" in response.json()


def test_checkout_champ_invalide() -> None:
    """Vérifier qu'un article avec un champ invalide est refusé.

    Returns:
        None: Le test réussit si l'API refuse la requête avec un détail d'erreur.

    Raises:
        AssertionError: Si le statut ou le corps de réponse diffère du contrat.
    """
    response = client.post(
        "/checkout", json={"items": [{"product_id": "toothbrush", "quantity": "2"}]}
    )

    assert response.status_code == 422
    assert "detail" in response.json()
