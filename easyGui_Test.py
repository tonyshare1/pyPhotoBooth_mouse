import easygui

result = easygui.enterbox(msg="Set Paper Number, New =18", title="Reload Paper Set", default ="18")
print( int(result))