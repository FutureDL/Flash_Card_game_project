import flet as ft

class FlashCard(ft.Container):
    def __init__(self, index, vocabulary, definition, example):
        super().__init__()
        self.index = index
        self.flipped = False

        # Index label (always pinned top-left)
        self.vocabIndex = ft.Text(value=str(self.index), size=30, color="grey", weight=ft.FontWeight.BOLD)

        # Front side (vocab centered)
        self.vocab = ft.Container(
            content=ft.Text(value=vocabulary, size=60, weight=ft.FontWeight.BOLD),
            alignment=ft.alignment.center,
            expand=True,
        )

        # Back side (vocab top-left, definition + example below)
        self.vocabInfo = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(value=vocabulary, size=40, weight=ft.FontWeight.BOLD),
                    self.labeled_divider("Definition"),  # line after vocab
                    ft.Text(value=definition, size=20, text_align=ft.TextAlign.LEFT),
                    self.labeled_divider("Example Sentence"),
                    ft.Text(value=example, size=20, text_align=ft.TextAlign.LEFT),
                ],
                alignment=ft.MainAxisAlignment.START,         # vertical: start from top
                horizontal_alignment=ft.CrossAxisAlignment.START,  # horizontal: align left
            ),
            alignment=ft.alignment.top_left,  # container aligns top-left
            padding=100,                       # 30px padding from edges
            expand=True
        )

        # A container that will switch between vocab and vocabInfo
        self.body = ft.Container(content=self.vocab, expand=True)

        # Stack ensures index is top-left, card body fills rest
        self.content = ft.Stack(
            controls=[
                ft.Container(content=self.body, expand=True),
                ft.Container(content=self.vocabIndex, left=10, top=10),  # pinned top-left
            ],
            expand=True,
        )

        self.expand = True
        self.on_click = self.handle_click

    def handle_click(self, e):
        # Toggle flip
        self.flipped = not self.flipped
        self.body.content = self.vocabInfo if self.flipped else self.vocab
        self.update()
        
    def labeled_divider(self, label: str):
            divider = ft.Row(
                controls=[
                    # ft.Container(content=ft.Divider(height=1, color="grey"),expand=True),
                    ft.Text(label, size=16, color="grey", weight=ft.FontWeight.BOLD),
                    ft.Container(content=ft.Divider(height=1, color="grey"),expand=True),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
            return divider

def main(page: ft.Page):
    page.title = "Flashcards"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    vocabulary = "hello"
    definition = "A word"
    example = "Hello world"
    num = 1

    vocab = FlashCard(num, vocabulary, definition, example)

    page.add(vocab)


if __name__ == "__main__":
    ft.app(target=main)