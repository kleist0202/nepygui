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

    vlayout = gui.VLayout(w, orientation="C")
    hlayout = gui.HLayout(w, orientation="C")
    gridlayout = gui.GridLayout(w, orientation="W")

    vlayout.add_widget(e2)
    vlayout.add_widget(e)

    gridlayout.add_widget(gui.Button(), 4, 4)
    gridlayout.add_widget(gui.Button(), 4, 0)
    gridlayout.add_widget(gui.Button(), 4, 0)
    gridlayout.add_widget(gui.Button(), 4, 2)
    gridlayout.add_widget(gui.Button(), 0, 4)
    gridlayout.add_widget(gui.Button(), 2, 4)
    gridlayout.add_widget(gui.Button(), 4, 4)
    gridlayout.add_widget(gui.Button(), 5, 1)

    val = 0
    for i in range(4):
        for j in range(4):
            bij = gui.Button(w=50, h=50, text=str(val), hover=True, gradient=True, fill=(200,10,1), gradientstart=(255,255,0), gradientend=(0,50,50))
            gridlayout.add_widget(bij, i, j)
            val += 1

    w.layouts.append(gridlayout)
    #w.layouts.append(hlayout)
    w.layouts.append(vlayout)
    w.main_loop()


if __name__ == "__main__":
    pygame.init()
    args = p.parse_args()
    main(args)
