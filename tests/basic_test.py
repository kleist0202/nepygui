import pygame
import argparse
from context import gui

p = argparse.ArgumentParser(formatter_class=argparse.MetavarTypeHelpFormatter)

def main(args):
    w = gui.Window(**vars(args))
    f = gui.Frame(x=200, w=100, gradient=True, hover=True, hovercolor=gui.Colors.Red)
    #b = gui.Button(x=200, y=200, w=100, h=100, text="yyyyy", hover=True, gradient=True, fill=(200,10,1))
    #print(b.get_size())
    w.widgets = [f]
    w.main_loop()

if __name__ == "__main__":
    pygame.init()
    args = p.parse_args()
    main(args)
