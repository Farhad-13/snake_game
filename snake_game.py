import tkinter as tk
import random

# Game Settings
WIDTH = 500
HEIGHT = 400
SIZE = 20

# Creating the Window
window = tk.Tk()
window.title("Snake Game")

apple_image = tk.PhotoImage(file="apple.png")
background_image = tk.PhotoImage(file="background.png")

# Fixed Window Size
window.geometry("600x550")
window.resizable(False, False)

# Prevent Full Screen with Alt + F10
window.bind("<Alt-F10>", lambda event: "break")

# Score
score = 0

# Game Status
game_started = False
game_over = False

# Movement Direction
direction = "Right"

# Snake
snake = [
    [100, 100],
    [80, 100],
    [60, 100]
]

# Creating the Canvas
canvas = tk.Canvas(
    window,
    width=WIDTH,
    height=HEIGHT,
    bg="black"
)

canvas.place(x=50, y=70)

# Displaying the Score
score_label = tk.Label(
    window,
    text="Score: 0",
    font=("Arial", 14)
)

score_label.place(x=270, y=45)


# Creating the Food
def create_food():
    x = random.randrange(0, WIDTH, SIZE)
    y = random.randrange(0, HEIGHT, SIZE)

    return [x, y]


food = create_food()


# Changing the Direction
def change_direction(new_direction):
    global direction

    if new_direction == "Up" and direction != "Down":
        direction = "Up"

    elif new_direction == "Down" and direction != "Up":
        direction = "Down"

    elif new_direction == "Left" and direction != "Right":
        direction = "Left"

    elif new_direction == "Right" and direction != "Left":
        direction = "Right"


# Drawing the Game
def draw():
    canvas.delete("all")

    canvas.create_image(
        0,
        0,
        image=background_image,
        anchor="nw"
    )

    # Drawing the Snake
    for part in snake:
        x = part[0]
        y = part[1]

        canvas.create_rectangle(
            x,
            y,
            x + SIZE,
            y + SIZE,
            fill="blue"
        )

    # Drawing the Food
    x = food[0]
    y = food[1]

    canvas.create_image(
        x + SIZE / 2,
        y + SIZE / 2,
        image=apple_image
    )


# Starting the Game
def start_game():
    global game_started

    game_started = True

    start_button.place_forget()

    move()


# Ending the Game
def game_over_screen():
    global game_over

    game_over = True

    canvas.create_rectangle(
        140,
        152,
        360,
        200,
        fill="white"
    )

    canvas.create_text(
        WIDTH / 2,
        HEIGHT / 2 - 20,
        text="GAME OVER!",
        fill="black",
        font=("Arial", 25)
    )

    restart_button.place(x=250,y=475)


# Moving the Snake
def move():
    global food
    global game_over
    global score

    if game_over:
        return

    # Snake Head
    head = snake[0]

    x = head[0]
    y = head[1]

    # Changing the Head Position
    if direction == "Up":
        y -= SIZE

    elif direction == "Down":
        y += SIZE

    elif direction == "Left":
        x -= SIZE

    elif direction == "Right":
        x += SIZE

    new_head = [x, y]

    # Collision with the Wall
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        game_over_screen()
        return

    # Collision with the Snake's Body
    if new_head in snake:
        game_over_screen()
        return

    # Adding a New Head to the Snake
    snake.insert(0, new_head)

    # If the Food Is Eaten
    if new_head == food:

        score += 1

        score_label.config(
            text="Score: " + str(score)
        )

        food = create_food()

    else:
        # Removing the Last Part of the Snake
        snake.pop()

    draw()

    # Next Move
    window.after(100, move)


# Restarting the Game
def restart_game():
    global snake
    global direction
    global food
    global score
    global game_over

    snake = [
        [100, 100],
        [80, 100],
        [60, 100]
    ]

    direction = "Right"

    score = 0

    game_over = False

    food = create_food()

    score_label.config(
        text="Score: 0"
    )

    restart_button.place_forget()

    draw()

    move()


# Close the Game
def close_game():
    window.destroy()


# Handle the Enter key
def enter_key(event):
    if not game_started:
        start_game()

    elif game_over:
        restart_game()


# Keyboard Controls
window.bind(
    "<Up>",
    lambda event: change_direction("Up")
)

window.bind(
    "<Down>",
    lambda event: change_direction("Down")
)

window.bind(
    "<Left>",
    lambda event: change_direction("Left")
)

window.bind(
    "<Right>",
    lambda event: change_direction("Right")
)

window.bind("<Return>", enter_key)
window.bind("<KP_Enter>", enter_key)

# Start Button
start_button = tk.Button(
    window,
    text="START",
    font=("Arial", 14),
    command=start_game
)

start_button.place(x=260,y=475)

# Restart Button
restart_button = tk.Button(
    window,
    text="RESTART",
    font=("Arial", 14),
    command=restart_game
)

# Close Button
close_button = tk.Button(
    window,
    text="✕",
    font=("Arial", 16, "bold"),
    fg="white",
    bg="red",
    activebackground="darkred",
    activeforeground="white",
    command=close_game,
    width=2,
    height=1,
    anchor="s"
)

close_button.place(x=560, y=0, width=40)

# Initial Display
draw()

window.mainloop()
