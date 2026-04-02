# Directions :
LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)

# Frames lists :
BTN_ONE_IMAGES = ["buttons/interactive_buttons1.1.png", 
                  "buttons/interactive_buttons1.2.png"]

BTN_TWO_IMAGES = ["buttons/interactive_buttons2.1.png", 
                  "buttons/interactive_buttons2.2.png"]

BTN_THREE_IMAGES = ["buttons/interactive_buttons3.1.png", 
                    "buttons/interactive_buttons3.2.png"]

BTN_FOUR_IMAGES = ["buttons/interactive_buttons4.1.png", 
                   "buttons/interactive_buttons4.2.png"]

BTN_FIVE_IMAGES = ["buttons/interactive_buttons5.1.png", 
                   "buttons/interactive_buttons5.2.png"]

BTN_SIX_IMAGES = ["buttons/interactive_buttons6.1.png", 
                   "buttons/interactive_buttons6.2.png"]

BTN_SEVEN_IMAGES = ["buttons/interactive_buttons7.1.png", 
                   "buttons/interactive_buttons7.2.png"]


# Configs :
BUTTON_CONFIGS = [
    {
        "images": BTN_ONE_IMAGES,
        "position": (850, 520),
        "reticle": "reticle_x",
        "direction": UP
    },
    {
        "images": BTN_TWO_IMAGES,
        "position": (700, 550),
        "reticle": "reticle_x",
        "direction": DOWN
    },
    {
        "images": BTN_THREE_IMAGES,
        "position": (500,550),
        "reticle": "reticle_x",
        "direction": LEFT
    },
    {
        "images": BTN_FOUR_IMAGES,
        "position": (230,430),
        "reticle": "reticle_x",
        "direction": RIGHT
    },
    {
        "images": BTN_FIVE_IMAGES,
        "position": (1000,540),
        "reticle": "reticle_y",
        "direction": UP
    },
    {
        "images": BTN_SIX_IMAGES,
        "position": (230,500),
        "reticle": "reticle_y",
        "direction": DOWN
    },
    {
        "images": BTN_SEVEN_IMAGES,
        "position": (520,55),
        "reticle": "reticle_y",
        "direction": LEFT
    },
]