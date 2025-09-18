import flet as ft
import FlashCardSet_v4 as CardSet
import time
import os
import ListWork_v2 as ff

class MainPage(ft.Container):
    def __init__(self, page:ft.Page):
        super().__init__()
        # Title of the APP
        self.title = ft.Container(
            content=ft.Text(value="Select a list to start with...", size=60, weight=ft.FontWeight.BOLD),
            bgcolor=ft.Colors.AMBER_100,
            padding=10,
            border_radius=20,
            expand=True
        )
        
        self.page = page
        
        # To first initalize the area for displaying lists, so it can be used in the displayList() function
        self.list_area = ft.Column(controls=[])
        
        # Whether in a list
        self.listopen = False
        
        self.last_refresh = 0
        
        # Button for adding list
        self.add_button = ft.FloatingActionButton(
            text="Add New List",
            icon=ft.Icons.ADD, 
            width=180, 
            height=100, 
            bgcolor=ft.Colors.ORANGE_300, 
            on_click = self.to_import_page
        )
        
        # Search bar
        self.search_bar = ft.TextField(
            hint_text="Enter the name of the list", 
            value="",
            label="Search for Vocab lists",
            on_change=self.searchList,
            min_lines=2, 
            max_lines=5
        )
        
        # Search result
        self.search_results = ft.Column(controls=[])
        
        # display the top area(greeting & add button)
        self.top_display = ft.Container(
            content=ft.Row(
                controls=[
                    self.title, 
                    self.add_button
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ), 
            alignment=ft.alignment.top_center
        )
        
        # Create the area for displaying games(currently no function)
        self.game_area = ft.Container(
            expand=3,
            padding=20,
            bgcolor=ft.Colors.GREY_200,
            border_radius=20,
            content = ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text("Game1", size=30, weight=ft.FontWeight.BOLD),
                        expand=True,
                        border_radius=20,
                        bgcolor=ft.Colors.GREY_50,
                        alignment = ft.alignment.center
                    ),
                    ft.Container(
                        content=ft.Text("Game2", size=30, weight=ft.FontWeight.BOLD),
                        expand=True,
                        border_radius=20,
                        bgcolor=ft.Colors.GREY_50,
                        alignment = ft.alignment.center
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
                spacing=20
            )
        )
        
        # Create the area for displaying vocabularies(initially with no lists)
        self.vocab_area = ft.Container(
            content=ft.Column(
                controls=[
                    self.search_bar,
                    ff.labeled_divider("Current Lists:"),
                ],
                expand=True,
            ),
            expand = 7,
            bgcolor=ft.Colors.GREY_100,
            padding= 20,
            border_radius= 20
        )
        
        # Creat the content area
        self.content_display = ft.Container(
            content=ft.Row(
                controls=[
                    # Left game area
                    self.game_area,
                    # Right vocab lists area
                    self.vocab_area
                ]
            ), 
            expand=True,
            alignment=ft.alignment.top_center
        )
        
        # Add the lists to the page
        current_directory = os.getcwd()# Get the current working directory
        print(f"Current directory: {current_directory}")

        folder_path = os.path.join(current_directory,"res/Vocab List") # Find the vocabulary excel documents
        self.Vocab_lists = ff.getLists(folder_path)
        self.displayList(self.Vocab_lists)
        
        # Add the page for import (initially invisible)
        import_text = ft.Container(
            content=ft.Text(value="Add a list from...", size=60, weight=ft.FontWeight.BOLD),
            bgcolor=ft.Colors.AMBER_100,
            padding=10,
            border_radius=20
        )
        generate_button = ft.FloatingActionButton(text="Generate From existing Lists", expand=True, on_click=self.generate_from_list)
        import_button = ft.FloatingActionButton(text="Import list", expand=True)
        
        quit_button = ft.FloatingActionButton(text="Return to home", on_click=self.return_to_home, expand=True)
        
        self.import_page = ft.Container(
            content = ft.Column(
                controls=[
                    import_text,
                    ft.Row(controls=[generate_button]),
                    ft.Row(controls=[import_button]),
                    ft.Row(controls=[quit_button])
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ), 
            expand= True,
            padding= 50,
            bgcolor=ft.Colors.ORANGE_100,
            visible = False
        )
        
        
        # the final display for the main page
        self.mainpage = ft.Column(
                controls=[
                    self.top_display,
                    self.content_display,
                    self.import_page
                ]
            )
        
        self.content = self.mainpage
        self.expand = True
        self.on_hover = self.refreshStatus
    
    # The functions for the buttons for the import page
    def to_import_page(self, e):
        self.import_page.visible = True
        self.top_display.visible = False
        self.content_display.visible = False
        self.mainpage.update()
        
    def return_to_home(self, e):
        self.import_page.visible = False
        self.top_display.visible = True
        self.content_display.visible = True
        self.mainpage.update()
    
    
    # Function for generating new lists from a previous list through the generate button
    # (Currently, it can only generate from the complete book list)
    # (In testing stage, the length is locked at 20, the number of lists generated is locked at 2)
    def generate_from_list(self,e):
        generate_num = 2
        generate_length = 20
        
        # Use the generate list function in the ListWork tool file
        new_lists = ff.generateList(self.Vocab_lists[0],generate_num,generate_length)
        # Add the new lists into the list for Vocab lists.
        for i in range(len(new_lists)):
            self.Vocab_lists.append(new_lists[i])
        self.displayList(self.Vocab_lists)
        
        # Return to the home page
        self.import_page.visible = False
        self.top_display.visible = True
        self.content_display.visible = True
        self.mainpage.update()
    
    # Function for starting the game from the game button 
    # (don't need to care currently, it won't work)
    def start_game(self):
        name = "Text List"
        launch_vocab = []
        launch_definition = []
        difficulty = 3
        
        vocab = []
        definition = []
        for i in self.Vocab_lists[1]:
            vocab.append(i[0])
            definition.append(i[1])
        launch_vocab.append(vocab)
        launch_definition.append(definition)
        
        try:
            import Game1_1BT as game
            self.Wrong_word_list = game.main(name, launch_vocab, launch_definition, difficulty, self.page)
            print("Finished_words: ",self.Wrong_word_list)
        except SystemExit:
            self.Wrong_word_list = game.global_wrong_word_list
            self.correct_num = game.global_correct_num
            self.wrong_num = game.global_wrong_num
            print("Finished_words: ",self.Wrong_word_list)

        self.appeared_num = self.Wrong_word_list[len(self.Wrong_word_list)-1]
        self.Wrong_word_list.pop(len(self.Wrong_word_list)-1)
        
        totalvocab = 0
        for i in launch_vocab:
            totalvocab += len(i)
        
        # Percentage = ((self.appeared_num - len(kinds)) / self.appeared_num) * 100
        if self.correct_num + self.wrong_num == 0:
            Percentage = float(0)
        else:
            Percentage = round((self.correct_num / (self.correct_num + self.wrong_num)) * 100, 2)
        print(f"\n Accuracy: {Percentage}%")
        
    # Function for displaying the loaded lists in the vocab area
    def displayList(self, Vocab_Lists:list):
        if self.list_area in self.vocab_area.content.controls:
            self.vocab_area.content.controls.remove(self.list_area)
        self.list_area = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[],
            expand=True, 
            spacing=10  
        )
        
        # Add the areas for lists
        for i in range(len(Vocab_Lists)):
            # Thee button to start studying the list
            button = ft.Container(content=ft.FloatingActionButton(
                text=f"Start", 
                data=i, 
                on_click=self.open_list, 
                bgcolor=ft.Colors.BLUE_100 if i != 0 else ft.Colors.BLUE_300, 
                width= 100,
                height= 50
            ))
            
            # The text before container(the list name)
            name = f"list{i+1}" if i != 0 else "Complete Word Book"
            list_name =  ft.Container(
                content=ft.Text(value=name, size=25),
                bgcolor=ft.Colors.BLUE_50 if i != 0 else ft.Colors.GREEN_100,
                padding=10,
                border_radius=20,
                expand=8 # takes up 8/10 of the length of the column
            )
            
            # The container area for each list
            list = ft.Container(
                content=ft.Row(
                    controls=[
                        list_name,
                        button
                    ],
                ), 
            )
            
            # Add the list to the display area
            self.list_area.controls.append(list)
        
        # Add to the main content container
        self.vocab_area.content.controls.append(self.list_area)
    
    def searchList(self, e):
        # Clear the search result area
        self.search_results.controls.clear()
        
        # Transform request into lower case
        search_request = self.search_bar.value.lower()
        
        # If there is search request...
        if search_request:
            # CHange the divider's label
            self.vocab_area.content.controls[1]=ff.labeled_divider(f"Results of '{search_request}':")
            
            # Clear the vocab area
            self.vocab_area.content.controls.pop()
            results = []
            
            # Find which list's name match
            for i in self.list_area.controls:
                if search_request.lower() in i.content.controls[0].content.value.lower():
                    results.append(i)
            
            # Add the matched lists into search result   
            for i in results:
                self.search_results.controls.append(i)
            
            # Add search result into content display container
            self.vocab_area.content.controls.append(self.search_results)
        else: 
            # CHange the divider's label
            self.vocab_area.content.controls[1]=ff.labeled_divider("Current Lists: ")
            
            # Clear the vocab area
            self.vocab_area.content.controls.pop()
            
            # Add the original list area into the content display container
            self.vocab_area.content.controls.append(self.list_area)
        self.update()
    
    # Function for opening a list through the "start" button
    def open_list(self, e):
        self.listopen = True # Indicate that a list is opened
        self.mainpage.controls = []
        # Find the vocab list that needs to be displayed
        self.current_set = CardSet.FlashCardSet(self.Vocab_lists[e.control.data])
        self.mainpage.controls.append(self.current_set)
        
        # Add the control buttons
        self.list_control_buttons = ft.Row(
            controls=[
                ft.FloatingActionButton(text="Return to home", on_click=self.close_list, expand=True),
                ft.FloatingActionButton(text="Finish List", on_click=self.close_list, expand=True)
            ]
        )
        # Disable the finish button if list is not completed first
        if(self.current_set.getStatus() != True):
            self.list_control_buttons.controls[1].disabled = True
            
        self.mainpage.controls.append(self.list_control_buttons)
        self.content.update()
    
    def refreshStatus(self,e):
        # Prevent too much refresh
        now = time.time()
        if now - self.last_refresh > 0.1:
            if(self.listopen == True): # Check the indication
                # Check if the user have reached the last page(以后会用文件记录数据，目前数据无法保存)
                if(self.current_set.getIndex() == self.current_set.getLength() or self.current_set.getStatus() == True):
                    # If yes enables the "finish" button
                    print(self.current_set.getIndex()," ", self.current_set.getLength())
                    self.list_control_buttons.controls[1].disabled = False
                else:
                    self.list_control_buttons.controls[1].disabled = True
                self.content.update()
            self.last_refresh = now
    
    # Closing the opened list
    def close_list(self,e):
        self.listopen == False
        self.mainpage.controls = []
        self.mainpage.controls.append(self.top_display)
        self.mainpage.controls.append(self.content_display)
        self.mainpage.controls.append(self.import_page)
        self.content.update()


def main(page: ft.Page):
    page.title = "FlashCardApp"
    page.window.width = 1100
    page.window.height = 780
    page.window.center()
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 30
    
    page.add(MainPage(page))

if __name__ == "__main__":
    ft.app(target=main)