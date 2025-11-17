from rest_framework.response import Response
from rest_framework.views import APIView
from core.application.dto.card_dto import CardDTO
from core.infrastructure.repositories.django_card_repository import DjangoCardRepository
from core.domain.services.card_service import CardService
from core.domain.models.card import Card

class CardView(APIView):

    def get(self, request):
        service = CardService(DjangoCardRepository())
        cards = service.list_cards()
        dto = CardDTO(cards, many=True)
        return Response(dto.data)

    def post(self, request):
        service = CardService(DjangoCardRepository())
        dto = CardDTO(data=request.data)
        dto.is_valid(raise_exception=True)

        card = Card(
            id=None,
            question=dto.validated_data["question"],
            answer=dto.validated_data["answer"],
            category=dto.validated_data["category"],
        )

        new_card = service.create_card(card)
        return Response(CardDTO(new_card).data)
