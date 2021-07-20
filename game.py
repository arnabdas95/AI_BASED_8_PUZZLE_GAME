from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import random

BACKGROUND_COLOR = '#7da0a8'
TEXT_COLOR = "#ffffff"
BUTTON_COLOR = '#133d33'
root = Tk()
root.title('8 puzzle Game')
root.resizable(height=False, width=False)
root.configure(background=BACKGROUND_COLOR)
root.geometry("471x700")
demo_image_list = ["assets/demo1.jpg", "assets/demo2.jpg", "assets/demo3.jpg"]
demo_tk_image_list = []
current_demo_image = "assets/demo1.jpg"

split_img_list = []
tk_photo_list = []
tk_photo_order = []
grid_button_list = []
sample_img_list = []
game_state = 'ready'


# select image in which puzzle will be played
def select_demo_img(*demo_number):
    global current_demo_image
    if demo_number:
        if demo_number[0] == 0:
            current_demo_image = demo_image_list[0]
            image_resetting(tk_photo_list, grid_button_list, split_img_list, shuffle_button)
        if demo_number[0] == 1:
            current_demo_image = demo_image_list[1]
            image_resetting(tk_photo_list, grid_button_list, split_img_list, shuffle_button)
        if demo_number[0] == 2:
            current_demo_image = demo_image_list[2]
            image_resetting(tk_photo_list, grid_button_list, split_img_list, shuffle_button)
    else:
        im = Image.open(demo_image_list[0])

#display sample demo image
def display_sample_image():
    global sample_img_list, temp, demo_tk_image_list
    # as local variable is not showing image as garbage collected by python
    for item in range(3):
        sample_img_list.append(Button(root, height=150, width=150, state='active', relief='solid'))
        sample_img_list[item].configure(command=lambda demo_number=item: select_demo_img(demo_number))
        sample_img_list[item].place(x=item * 157, y=545)
        x = Image.open(demo_image_list[item])
        demo_tk_image_list.append(ImageTk.PhotoImage(x.resize((150, 150))))
        sample_img_list[item].configure(image=demo_tk_image_list[item])


# reset everything after button click or new puzzle image is set
def image_resetting(tk_photo_list, grid_button_list, split_img_list, shuffle_button):
    global blank_tile_row, blank_tile_col,game_state
    split_img_list.clear()
    tk_photo_list.clear()
    tk_photo_order.clear()
    blank_tile_row, blank_tile_col=2,2
    split_image(3)

    grid_count = 0
    for i in split_img_list:
        grid_button_list[grid_count].destroy
        grid_count += 1

    grid_button_list.clear()
    tk_display()
    game_state='ready'
    shuffle_button.configure(state='active')



# convert pillow image to tkinter image
def pil_to_tk_img(tk_photo_list, tk_photo_order):
    grid_count = 0
    for i in split_img_list:
        tk_photo_list.append(ImageTk.PhotoImage(i))
        tk_photo_order.append(str(tk_photo_list[grid_count]))
        grid_count += 1


# crop or divide the image into 8 part
def split_image(grid_size):
    im = Image.open(current_demo_image)
    out = im.resize((450, 450))
    for i in range(grid_size):
        for j in range(grid_size):
            box = (j * 150, i * 150, (j + 1) * 150, i * 150 + 150)
            split_img_list.append(out.crop(box))

    # make last grid blank by filling only color
    blank_img = Image.new(mode="RGB", size=(150, 150), color=BUTTON_COLOR)
    split_img_list[-1] = blank_img
    pil_to_tk_img(tk_photo_list, tk_photo_order)


# display the puzzle grid
def tk_display():
    grid_count = 0
    for i in range(3):
        for j in range(3):
            grid_button_list.append(
                Button(root, image=tk_photo_list[grid_count], text='', compound="center", fg=TEXT_COLOR,
                       height=150, width=150, state='active',
                       relief='solid', command=lambda row=i, column=j: slide_tile(row, column)))
            grid_button_list[grid_count].grid(row=i, column=j)
            grid_count += 1


# shuffle  the display grid
def shuffle_grid(grid_button_list):
    global game_state
    grid_count = 0
    demo_list = [i for i in range(len(grid_button_list))]
    random.shuffle(demo_list)
    for i in (demo_list):
        grid_button_list[i].configure(image=tk_photo_list[grid_count])
        grid_count += 1
    get_blank_tile_row_col(grid_button_list, tk_photo_list, 3)
    shuffle_button.configure(state='disabled', bg=BACKGROUND_COLOR)
    game_state = 'active'
    if grid_button_list[0].cget('text') != '':
        show_number()


# grid number displaying
def show_number():
    global tk_photo_order
    if grid_button_list[0].cget('text') == '':
        for item in grid_button_list:
            val = (item.cget('image'))
            val = tk_photo_order.index(val)
            item.configure(text=val + 1)
    else:
        for item in grid_button_list:
            item.configure(text='')


# game end check
def check_game_success(tk_photo_list, grid_button_list, game_state):
    for item in range(len(tk_photo_list)):
        if str(tk_photo_list[item]) != str(grid_button_list[item].cget('image')):
            print('false')
            return False
    game_state = 'win'
    print('Win')
    return True


# get the blank tile row and column
def get_blank_tile_row_col(grid_button_list, tk_photo_list, grid_size):
    grid_count = 0
    global blank_tile_row, blank_tile_col
    for i in range(grid_size):
        for j in range(grid_size):
            if grid_button_list[grid_count].cget('image') == str(tk_photo_list[8]):
                blank_tile_row, blank_tile_col = i, j
            grid_count += 1

#move the tile up down left right
def slide_tile(row, column):
    global blank_tile_row, blank_tile_col, game_state
    if game_state == 'active':
        temp_grid_img = grid_button_list[row * 3 + column].cget('image')
        if blank_tile_row == row and blank_tile_col + 1 == column:
            grid_button_list[row * 3 + column].configure(image=tk_photo_list[-1])
            grid_button_list[blank_tile_row * 3 + blank_tile_col].configure(image=temp_grid_img)
            blank_tile_row, blank_tile_col = row, column

        # slide right
        if blank_tile_row == row and blank_tile_col - 1 == column:
            grid_button_list[row * 3 + column].configure(image=tk_photo_list[-1])
            grid_button_list[blank_tile_row * 3 + blank_tile_col].configure(image=temp_grid_img)
            blank_tile_row, blank_tile_col = row, column

        # slide top
        if blank_tile_col == column and blank_tile_row + 1 == row:
            grid_button_list[row * 3 + column].configure(image=tk_photo_list[-1])
            grid_button_list[blank_tile_row * 3 + blank_tile_col].configure(image=temp_grid_img)
            blank_tile_row, blank_tile_col = row, column

        # slide down
        if blank_tile_col == column and blank_tile_row - 1 == row:
            grid_button_list[row * 3 + column].configure(image=tk_photo_list[-1])
            grid_button_list[blank_tile_row * 3 + blank_tile_col].configure(image=temp_grid_img)
            blank_tile_row, blank_tile_col = row, column

        #update the grid number
        if grid_button_list[0].cget('text') != '':
            for item in grid_button_list:
                val = (item.cget('image'))
                val = tk_photo_order.index(val)
                item.configure(text=val + 1)
        check_game_success(tk_photo_list, grid_button_list, game_state)


# button declare
shuffle_button = Button(root, height=2, width=25, state='active', relief='solid', bg=BUTTON_COLOR, text="Shuffle",
                        command=lambda grid_button_list=grid_button_list: shuffle_grid(grid_button_list))
restart_button = Button(root, height=2, width=25, bg=BUTTON_COLOR, text='Reset', state='active', relief='solid',
                        command=lambda tk_photo_list=tk_photo_list, grid_button_list=grid_button_list,
                                       split_img_list=split_img_list, shuffle_button=shuffle_button: image_resetting(
                            tk_photo_list, grid_button_list, split_img_list, shuffle_button))
show_number_button = Button(root, height=2, width=18, bg=BUTTON_COLOR, text='Toggle Number', state='active', relief='solid',
                            command=show_number)
shuffle_button.place(x=0, y=470)
restart_button.place(x=285, y=470)
show_number_button.place(x=165, y=470)

# main
if __name__ == '__main__':
    split_image(3)
    display_sample_image()
    tk_display()

root.mainloop()
