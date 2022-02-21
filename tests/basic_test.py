import pygame
import argparse
from context import gui

p = argparse.ArgumentParser(formatter_class=argparse.MetavarTypeHelpFormatter)

def main(args):
    w = gui.Window(**vars(args))
    f = gui.TextFrame(fontsize=12,text="ddddddddd", x=200, w=100, fill=gui.Colors.Black, gradient=True, gradientstart=(0,0,255), gradientend=(0,255,0), hover=True, hovercolor=gui.Colors.Red)
    b = gui.Button(x=200, y=200, w=100, h=100, text="yyyyy", hover=True, gradient=True, fill=(200,10,1))
    e = gui.EntryWidget(x=400, y=400, w=200, h=60, borderthickness=6)
    e2 = gui.EntryWidget(x=400, y=200, w=200, h=60)

    vb1 = gui.Button(w=100, h=50, text="1", fill=(200,10,1))
    vb2 = gui.Button(w=100, h=50, text="2", fill=(200,10,1))

    vlayout = gui.VLayout(w, orientation="C", x_start=10)
    hlayout = gui.HLayout(w, orientation="W")
    vlayout.add_widget(vb1, 10)
    vlayout.add_widget(vb2, 20)
    vlayout.add_widget(e2, 10)
    vlayout.add_widget(gui.Button(w=25, h=10))

    hlayout.add_widget(gui.Button(w=25, h=10))
    hlayout.add_widget(gui.Button(w=25, h=10))
    hlayout.add_widget(vb1)

    gridlayout = gui.GridLayout(w, orientation="W")

    #gridlayout.add_widget(gui.Button(), 4, 4)
    #gridlayout.add_widget(gui.Button(), 4, 0)
    #gridlayout.add_widget(gui.Button(), 5, 0)
    #gridlayout.add_widget(gui.Button(), 5, 2)

    #val = 0
    #for i in range(4):
    #    for j in range(4):
    #        bij = gui.Button(w=20, h=20, text=str(val), hover=True, gradient=True, fill=(200,10,1))
    #        gridlayout.add_widget(bij, i, j)
    #        val += 1

    #w.layouts.append(gridlayout)
    w.layouts.append(hlayout)
    w.main_loop()


if __name__ == "__main__":
    pygame.init()
    args = p.parse_args()
    main(args)
