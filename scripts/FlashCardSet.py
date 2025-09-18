import flet as ft
import scripts.FlashCard as FlashCard

class FlashCardSet(ft.Container):
    def __init__(self, vocab_list):
        super().__init__()
        # Add the flashcards into the set
        self.flashcards = []
        
        for i in range(len(vocab_list)):
            vocab = FlashCard.FlashCard(i+1, vocab_list[i][0], vocab_list[i][1], vocab_list[i][2])
            self.flashcards.append(vocab)
        
        # Initiial position at first card
        self.current_card = self.flashcards[0]
        self.index = 0
        
        # Initial complete status is false
        self.completed = False
        
        # Two buttons for directing the set
        self.left_button = ft.FloatingActionButton(icon=ft.Icons.ARROW_LEFT, on_click= self.Last_Card)
        self.right_button = ft.FloatingActionButton(icon=ft.Icons.ARROW_RIGHT, on_click= self.Next_Card)
        
        # THe main display container
        self.Display = ft.Container(
            content=ft.Row(
                controls=[
                    self.left_button,
                    ft.Container(content = self.current_card,expand=True),
                    self.right_button
                ],expand=True
            ),
            bgcolor = ft.Colors.GREY_200,
            border_radius = 20,
            padding = 10,
            expand=True
        )
        self.expand = True
        self.content = self.Display
        
        self.bgcolor = ft.Colors.GREY_100
        self.border_radius = 20
    
    # The function for navigating toward the last card   
    def Last_Card(self, e):
        try:
            self.current_card = self.flashcards[self.index - 1]
            self.index -= 1
            self.Display.content.controls[1].content = self.current_card
            self.Display.update()
        except IndexError:
            pass
    
    # The function for navigating toward the next card  
    def Next_Card(self, e):
        try:
            self.current_card = self.flashcards[self.index + 1]
            self.index += 1
            self.Display.content.controls[1].content = self.current_card
            self.Display.update()
        except IndexError:
            self.completed = True
    
    # The function for getting the current completion status    
    def getStatus(self):
        if(self.getLength() == self.getIndex()):
            self.completed = True
        return self.completed
    
    def getLength(self):
        return len(self.flashcards)
    
    def getIndex(self):
        return self.index+1