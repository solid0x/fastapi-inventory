from models import Item


class StubItemStore:
    def __init__(self):
        self.items = [Item(id=1, name="stub_item 1")]

    async def get_items(self) -> list[Item]:
        return self.items

    async def get_item(self, id: int) -> Item:
        found_items = [i for i in self.items if i.id == id]
        if found_items:
            return found_items[0]

    async def create_item(self, name: str) -> Item:
        id = len(self.items) + 1
        new_item = Item(id=id, name=name)
        self.items.append(new_item)
        return new_item
