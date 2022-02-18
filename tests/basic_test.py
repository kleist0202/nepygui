import pygame
import argparse
from context import gui

p = argparse.ArgumentParser(formatter_class=argparse.MetavarTypeHelpFormatter)

def main(args):
    w = gui.Window(**vars(args))
    f = gui.Frame(x=200, w=100, fill=gui.Colors.Black, gradient=True, gradientstart=(0,0,255), hover=True, hovercolor=gui.Colors.Red)
    b = gui.Button(x=200, y=200, w=100, h=100, text="yyyyy", hover=True, gradient=True, fill=(200,10,1))
    e = gui.EntryWidget(x=400, y=400, w=200, h=60, borderthickness=6)
    e2 = gui.EntryWidget(x=400, y=200, w=200, h=60, borderthickness=6)
    g = gui.Gradient((100,105,0), (0,150,200), 100, 100)

    w.widgets = [f, b, e, e2]
    w.surfaces = [g.get_surface(),]
    w.main_loop()

if __name__ == "__main__":
    pygame.init()
    args = p.parse_args()
    main(args)
