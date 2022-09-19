from ursina import *

app = Ursina()

camera.orthographic = True
camera.fov =4
camera.positon = (1,1)
Text.default_resolution *=2

player = Entity(name='o',color =color.azure)
cursor = Tooltip(player.name, color = player.color, origin = (0,0), scale =4, enabled = True)
cursor.background.color = color.clear
bg = Entity(parent=scene, model='quad',texture = 'shore',scale = (16,8), z=10, color = color.red)
mouse.visible = False

#create a matrix to store buttons in. makes it easier to check for victoty

board =[[None for x in range(3)] for y in range(3)]

for y in range(3):
    for x in range(3):
        b = Button(parent=scene, postion = (x,y))
        board[x][y] = b
        
        def on_click(b=b):
            b.text = player.name
            b.color = player.color
            b.collision = False
            
            if player.name =='o':
                player.name ='x'
                player.color = color.orange
            else:
                player.name = 'o'
                player.color = color.azure
            cursor.text = ''
            cursor.color=player.color
        b.on_click=on_click
        
def check_for_victory():
    name = player.name
won = (
       (board[0][0].text == name and board[1][0].text == name and board[2][0].text == name)
       (board[0][1].text == name and board[1][1].text == name and board[2][1].text == name)
       (board[0][2].text == name and board[1][2].text == name and board[2][2].text == name)
       (board[0][0].text == name and board[0][1].text == name and board[0][2].text == name)
       (board[1][0].text == name and board[1][1].text == name and board[1][2].text == name)
       (board[2][0].text == name and board[2][1].text == name and board[2][2].text == name)
       (board[0][0].text == name and board[1][1].text == name and board[2][2].text == name)
       (board[0][2].text == name and board[1][1].text == name and board[2][0].text == name)
)

if won:
    print('winner is:', name)
    destroy(cursor)
    mouse.visibile = True
    Panel(z=1, scale = 10, model='quad')
    t= Text(f'player\n{name}\nwon!',scale =3 , origin =(0,0),background=True)
    t.create_background(padding=(.5,.25),radius = Text.size/2)
    t.background.color = player.color.tint(-.2)
    
app.run()