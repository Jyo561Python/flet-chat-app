import flet
from flet import Checkbox, Column, FloatingActionButton,margin, Page, Row, TextField, UserControl, icons, padding, Container,alignment,Text,KeyboardEvent, ListView
import socketio

class TodoApp(UserControl):
    def build(self):
        self.new_task = TextField(color="white",border_color="white")
        self.tasks = Column()
        self.joined = False
        self.currentUser = ""
        self.text=""
        self.ids=1
        self.messages=[
            {
                "id":1,
                "text":'Hey, how are you',
                "user":"Manoj"
            },
        ]
        # application's root control (i.e. "view") containing all other controls
        self.punter = Container(
            content=Column(
            controls=[
                Row(
                    alignment="center",
                    controls=[
                        self.new_task,
                    ],
                ),
                Row(
                    alignment="center",
                    controls=[
                        FloatingActionButton("Login", on_click=self.join),
                    ],
                ),
            ],
        ),
        margin=100,    )
        self.punter.margin=margin.only(top=400)
        self.show_messages=Column(scroll="hidden",auto_scroll=True,height=800)
        self.message=TextField(hint_text="Write your message",border_color="white",expand=True,max_lines=2,on_submit=self.on_keyboard)
        # messages=Container(
        #     margin=300,
        #     content=Column(
                
        #         controls=[
        #             Row(
        #                 alignment="center",
        #                 controls=[
                            
        #                 ]
        #             )
        #         ],
        #     ),)

        self.chat=Container(
            content=Column(
                controls=[
                    Container(
                        Column(
                            [
                                self.show_messages
                            ],
                            
                        )
                    ),
                    Container(
                        content=Row(
                            controls=[
                                self.message,
                            ]
                        ),
                        margin=margin.only(top=40),
                    )
                ],
                alignment="spaceBetween",
                expand=True
            ),
        )
        #self.punter.visible=False
        for m in self.messages:
            self.show_messages.controls.append(Text(f"{m['user']} : {m['text']}",color="white"))
        self.chat.visible=False
        self.showpop=Container(
           content=Column(
               controls=[
                           self.punter,
                           self.chat
               ],
           ),
           )
        return self.showpop

    async def on_keyboard(self,e: KeyboardEvent):
        textval=self.message.value
        self.message.value=""
        self.show_messages.controls.append(Text(f"{self.currentUser} : {textval}",color="white"))
        self.ids+=1
        obj={
            "id":self.ids,
            "text":textval,
            "user":self.currentUser
        }
        self.messages.append(obj)
        print(self.messages)

        self.update()
        await self.sio.emit('message',{'data':obj})


    async def join(self,e):
        self.currentUser=self.new_task.value
        print(self.currentUser)
        self.joined=True
        self.chat.visible=True
        self.punter.visible=False
        self.sio=socketio.AsyncClient()
        await self.sio.connect('http://127.0.0.1:8000')
        siok=self.sio
        @siok.on('message:received')
        async def addon(event, sid, data):
            self.show_messages.controls.append(Text(f"{mydata.user} : {mydata.text}",color="white"))
            self.messages.append(mydata)
        self.update()


def main(page: Page):
    page.title = "ToDo App"
    page.horizontal_alignment = "center"
    #page.bgcolor ="white"
    page.scroll=True
    page.window_resizable = True

    # create application instance
    todo = TodoApp()
    # add application's root control to the page
    page.content=""
    page.add(todo)

    page.update()

flet.app(target=main, view=flet.WEB_BROWSER)