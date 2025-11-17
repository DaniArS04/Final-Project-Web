
class CardService:
    def __init__(self, repository):
        self.repository = repository

    def list_cards(self):
        return self.repository.get_all()

    def create_card(self, card):
        return self.repository.save(card)
