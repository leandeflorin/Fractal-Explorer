"""
Fractal explorer
By Lean Deflorin (cantact me at leandeflorin@gmail.com for questions!)

This program visualiszes the Mandelbrot set and allows users to explore 
the related Julia sets. It was a lot of fun to write, and to be able to expand
from my Code in Place knowledge, by learning Tkinter. 

Feel free to use any part of this code, as well as modifying or optimising it,
you have my permission to do whatever you want with it.
"""

#Imports
import tkinter as tk
import math

# constants and globals
WIDTH = 800
HEIGHT = 800

"""
Initial complex plane boundaries, this is where the interesting stuff happens.
This is the usual range that is used in Mandelbrot visualisation
"""
RE_START, RE_END = -2, 2
IM_START, IM_END = -2, 2

# Global variables for zoom
zoom_rect = None
start_x = start_y = None

"""
The idea is that the user gets to decide the amount of iterations, 
and ive set the range between 3 and 300 as they all give interesting results, 
there isnt really a poin going beyond that and choosing low numbers are not a good
representation of the mandelbrot set but a fun way to explore the limits of the program. 
It also designed to always respond, until the user imput is a valid number in the given range.
"""
def iterations():
    while True:
        user_input = input("Enter number of iterations (3 to 300): ")
        try:
            maxint = int(user_input)
            if 3 <= maxint <= 300:
                print("Creating fractal magic... can take up to a minute :)")
                return maxint
            else:
                print("Please enter a number between 3 and 300.")
        except ValueError:
            print("That's not a number!")

# This was one of the first things I wrote, and it took waaay too long for the complexity
def draw_mandelbrot(canvas, max_iter):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            zx = RE_START + (x / WIDTH) * (RE_END - RE_START)
            zy = IM_START + (y / HEIGHT) * (IM_END - IM_START)
            z = complex(zx, zy)
            c = z
            iteration = 0

            while abs(z) <= 2 and iteration < max_iter:
                z = z*z + c
                iteration += 1

            color = get_color(iteration, max_iter)
            canvas.create_line(x, y, x + 1, y, fill=color)
    print("Enjoy!")

"""
I needed it for the mandelbrot set, was fun to write, 
honestly I looked up parts of the code.
But it quite facinating how easy it is to map pixel to complex numbers
"""
def pixel_to_complex(x, y):
    real = RE_START + (x / WIDTH) * (RE_END - RE_START)
    imag = IM_START + (y / HEIGHT) * (IM_END - IM_START)
    return complex(real, imag)

"""
Draws the corresponding Julia set to the pixel you click on,
based on the draw_mandelbrot function, with a few tweaks
"""
def draw_julia(canvas, c, max_iter):
    print("Generating the Julia set of your choice...")
    re_start, re_end = -2, 2
    im_start, im_end = -2, 2

    for x in range(WIDTH):
        for y in range(HEIGHT):
            real = re_start + (x / WIDTH) * (re_end - re_start)
            imag = im_start + (y / HEIGHT) * (im_end - im_start)
            z = complex(real, imag)
            iteration = 0

            while abs(z) <= 2 and iteration < max_iter:
                z = z*z + c
                iteration += 1

            color = get_color(iteration, max_iter)
            canvas.create_line(x, y, x + 1, y, fill=color)
    print("Done!")

#
def on_click(event, canvas, max_iter):
    canvas.delete("all")
    c = pixel_to_complex(event.x, event.y)
    draw_julia(canvas, c, max_iter)
    #The unbinding is necessary so that the user cant generate a Julia set of a Julia set
    canvas.unbind("<Button-1>")
    canvas.unbind("<ButtonPress-3>")
    canvas.unbind("<B3-Motion>")
    canvas.unbind("<ButtonRelease-3>")


def on_mouse_down(event):
    global start_x, start_y, zoom_rect
    start_x, start_y = event.x, event.y
    zoom_rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="white")


def on_mouse_drag(event):
    global zoom_rect
    # Maintain square aspect ratio
    dx = event.x - start_x
    dy = event.y - start_y
    side = min(abs(dx), abs(dy))
    end_x = start_x + side if dx >= 0 else start_x - side
    end_y = start_y + side if dy >= 0 else start_y - side
    canvas.coords(zoom_rect, start_x, start_y, end_x, end_y)
    

#One of the most complex parts of the code, inspired by a video and tutorial on how to do it
def on_mouse_up(event, canvas, max_iter):
    global RE_START, RE_END, IM_START, IM_END
    x0, y0 = start_x, start_y
    x1, y1 = canvas.coords(zoom_rect)[2:]

    if x0 == x1 or y0 == y1:
        return

    x_min, x_max = sorted([x0, x1])
    y_min, y_max = sorted([y0, y1])

    new_re_start = RE_START + (x_min / WIDTH) * (RE_END - RE_START)
    new_re_end = RE_START + (x_max / WIDTH) * (RE_END - RE_START)
    new_im_start = IM_START + (y_min / HEIGHT) * (IM_END - IM_START)
    new_im_end = IM_START + (y_max / HEIGHT) * (IM_END - IM_START)

    RE_START, RE_END = new_re_start, new_re_end
    IM_START, IM_END = new_im_start, new_im_end

    canvas.delete("all")
    draw_mandelbrot(canvas, max_iter)

"""
An attempt of creating a color picker which feels intuitive,
and gives a good looking result, feel free to modify, add or remove
colors after yout liking. 
"""
def pick_color(t, colors):
    if t <= 0:
        return colors[0]
    if t >= 1:
        return colors[-1]

    scaled_t = t * (len(colors) - 1)
    i = int(scaled_t)
    frac = scaled_t - i

    r1, g1, b1 = colors[i]
    r2, g2, b2 = colors[i + 1]

    r = int(r1 + (r2 - r1) * frac)
    g = int(g1 + (g2 - g1) * frac)
    b = int(b1 + (b2 - b1) * frac)

    return (r, g, b)


def get_color(iteration, max_iter):
    t = iteration / max_iter
    colors = [
        (15, 10, 30),    # almost black
        (128, 0, 128),   # deep purple
        (255, 0, 0),     # red
        (255, 128, 0),   # orange
        (220, 230, 23),  # soft yellow
        (0, 3, 10)       #darkness 
    ]
    r, g, b = pick_color(t, colors)
    return f'#{r:02x}{g:02x}{b:02x}'


def reset_to_mandelbrot(canvas, max_iter):
    global RE_START, RE_END, IM_START, IM_END
    RE_START, RE_END = -2, 2
    IM_START, IM_END = -2, 2
    canvas.delete("all")
    draw_mandelbrot(canvas, max_iter)
    #When the user returns to the start, they should be able to explore once again,
    #hence the binding of the clicks
    canvas.bind("<Button-1>", lambda event: on_click(event, canvas, max_iter))
    canvas.bind("<ButtonPress-3>", on_mouse_down)
    canvas.bind("<B3-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-3>", lambda event: on_mouse_up(event, canvas, max_iter))



def create_window(max_iter):
    root = tk.Tk()
    root.title("Fractal Explorer")
    global canvas
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
    canvas.pack()

    button = tk.Button(root, text="Back to Mandelbrot", bg="gray20", fg="white",
                       font=("Helvetica", 10, "bold"),
                       command=lambda: reset_to_mandelbrot(canvas, max_iter))
    button.pack(pady=6)

    # Bind mouse interactions
    canvas.bind("<Button-1>", lambda event: on_click(event, canvas, max_iter))
    canvas.bind("<ButtonPress-3>", on_mouse_down)
    canvas.bind("<B3-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-3>", lambda event: on_mouse_up(event, canvas, max_iter))

    return root, canvas

#Where everything happens, I tried to be as clear as possible without overcroudning the user with information.
def main():
    print("Welcome to this fractal viewer.")
    print("Fractals are complex geometric shapes, often based on interesting math!")
    print("This program explores two of the most famous fractals:")
    print("The Mandelbrot set and the Julia set.")
    print("Due to the complexity of the fractals, generation can take time,")
    print("so be patient!")
    print("First we have to define the number of iterations,")
    print("which determines how detailed the fractal gets.")
    max_iter = iterations()
    root, canvas = create_window(max_iter)
    draw_mandelbrot(canvas, max_iter)
    print("Left-click to explore Julia sets. Right-click and drag to zoom into Mandelbrot.")
    root.mainloop()

main()
