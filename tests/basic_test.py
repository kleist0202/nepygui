import pygame
import argparse
import nepygui

p = argparse.ArgumentParser(formatter_class=argparse.MetavarTypeHelpFormatter)

def main(args):
    w = nepygui.Window(**vars(args))
    f = nepygui.TextFrame(fontsize=12,text="ddddddddd", x=200, w=100, fill=nepygui.Colors.Black, gradient=True, gradientstart=(0,0,255), gradientend=(0,255,0), hover=True, hovercolor=nepygui.Colors.Red)
    b = nepygui.Button(x=200, y=200, w=100, h=100, text="yyyyy", hover=True, gradient=True, fill=(200,10,1))
    e = nepygui.EntryWidget(x=400, y=400, w=200, h=60, borderthickness=6)
    e2 = nepygui.EntryWidget(x=400, y=200, w=200, h=60)

    vlayout = nepygui.VLayout(w, orientation="C")
    hlayout = nepygui.HLayout(w, orientation="C")
    gridlayout = nepygui.GridLayout(w, orientation="W")

    vlayout.add_widget(e2)
    vlayout.add_widget(e)

    gridlayout.add_widget(nepygui.Button(), 4, 4)
    gridlayout.add_widget(nepygui.Button(), 4, 0)
    gridlayout.add_widget(nepygui.Button(), 4, 0)
    gridlayout.add_widget(nepygui.Button(), 4, 2)
    gridlayout.add_widget(nepygui.Button(), 0, 4)
    gridlayout.add_widget(nepygui.Button(), 2, 4)
    gridlayout.add_widget(nepygui.Button(), 4, 4)
    gridlayout.add_widget(nepygui.Button(), 5, 1)

    val = 0
    for i in range(4):
        for j in range(4):
            bij = nepygui.Button(w=50, h=50, text=str(val), hover=True, gradient=True, fill=(200,10,1), gradientstart=(255,255,0), gradientend=(0,50,50))
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
