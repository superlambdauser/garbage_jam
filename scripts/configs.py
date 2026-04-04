# Directions :
LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)

DIRECTIONS = [LEFT, RIGHT, UP, DOWN]

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

BTN_EIGHT_IMAGES = ["buttons/interactive_buttons8.1.png", 
                   "buttons/interactive_buttons8.2.png"]

BTN_NINE_IMAGES = ["buttons/interactive_buttons9.1.png", 
                   "buttons/interactive_buttons9.2.png"]

BTN_TEN_IMAGES = ["buttons/interactive_buttons10.1.png", 
                   "buttons/interactive_buttons10.2.png"]

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
    {
        "images": BTN_EIGHT_IMAGES,
        "position": (770,405),
        "reticle": "reticle_y",
        "direction": RIGHT
    },
    # DECOYS :
    {
        "images": BTN_NINE_IMAGES,
        "position": (140,550),
        "reticle": None,
        "direction": None
    },
    {
        "images": BTN_TEN_IMAGES,
        "position": (320,440),
        "reticle": None,
        "direction": None
    },
]


# RED BUTTON
RED_BTN_IMAGES = ["buttons/red_button_off.png",
                  "buttons/red_button_on.png",
                  "buttons/red_button_pressed.png"]

RED_BUTTON_CONFIG = {
        "images": RED_BTN_IMAGES,
        "position": (590, 520),
        "reticle": "reticle_x",
        "direction": UP
    }

# START BUTTON 
START_BTN_IMAGES = ["buttons/start_btn.png",
                    "buttons/start_btn.png",
                    "buttons/start_btn_pressed.png"]

START_BTN_CONFIG = {
    "images":START_BTN_IMAGES,
    "position":(590,550),
    
}

# RESTART BUTTON 
RESTART_BTN_IMAGES = ["buttons/restart_button.png",
                      "buttons/restart_button2.png"]

RESTART_BTN_CONFIG = {
    "images":RESTART_BTN_IMAGES,
    "position":(600,400),
    
}

# POST ITS :
POST_IT_LEFT_CONFIGS = [
    # LEFT
    {
        "image": "post_its/post_it_with_clear_instructions.png",
        "position": (50,200)
    },
    {
        "image": "post_its/post_it_shmile.png",
        "position" : (100,300)
    }
]
POST_IT_RIGHT_CONFIGS = [
    {
        "image": "post_its/post_it_OXO.png",
        "position" : (1100,250)
    },
    {
        "image": "post_its/post_it_family.png",
        "position" : (1150,115)
    },
]