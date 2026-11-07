
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QTextBrowser)
from pathlib import Path

class HelpWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("WAFC - Help")
        self.resize(1500, 800)

        layout = QVBoxLayout(self)

        help_text = QTextBrowser()
        wynnpic = Path(__file__).parent / "Wynn stats SC.png"
        WAMCpic = Path(__file__).parent / "WAFC stats SC.png"

        help_text.setHtml("""
            <h1>Welcome to Wynncraft Animal Food Calculator</h1>

            <h2>How to use:</h2>
            <p>There are two main ways to calculate materials. Either the calculation will only use lvl.1 materials or it will use the highest possible ingredients for the mount. 
            Choose which mode you prefer by selecting the apropiate option in the dropdown selection. <br>
            Insert the stats of your mount into the boxes and press "Go". This will then Output the optimized amounts of each material to get to the maximum potential of the mount.</p>

            <h2>FAQ:</h2>
            <p>Q: What numbers do I use? <br>
            A: there are 3 rows of stats, one of which is only necessary if you want to use higher level materials. <br></p>
            <img src="{}" width="300">
            <img src="{}" width="1000">
            <p>In Wynncraft the numbers shown as "Level" are the numbers you need to insert as "training level" in WAFC; "Limit" goes to "current value"; "Max" goes to "max potential"; as shown in the example above. <br>
            If you only use the lvl 1 materials, the first row (aka the "level") is irrelevant and hence not shown.<br><br>
            Q: I cant see all the stats I need. Why? <br>
            A: To be able to see all required stats you need to place the mount in its appropriate enclosure, otherwise (i.e. in your inventory or in the bank) you will only see "Level" and "Limit". <br> <br>
            Q: How do mounts work... like in generall? <br>
            A: Mounts have 3 types of stat. The Max value shows the absolut highest a stat can go for this specific mount. This value can't change. <br>
            The "limit" shows the soft-cap of the mount. This stat gets increased by feeding the mount the appropriate food in its enclosure. This is capped at the respective Max value<br>
            The "Level" shows what the mounts current level in any given stat is. This is capped at whatever the "limit" is at the current time. This stat gets upgraded by collecting the respective pop-ups while riding the mount<br>
            To get a mount with higher "Max" values you need to breed your mounts. You do this by "feeding" a mount to another mount. Both mounts need to have reached a certain "limit" before being able to breed. The "Max" values for the resulting mount are the average of both parents' "limit" +/- variance. Hence to get the best results it is best to fully max your mounts "limits" before breeding and only breed mounts of similar max potential. <br><br>
            Q: Are those genuinly frequently asked? <br>
            A: No, i havent been asked anything, but I want to preemptively answer any question I can think of <br> <br>
            Q: Why is this such a mess? <br>
            A: Because I am not a professional and this app was initially only intended for my personal use <br> </p>

            <h2>disclaimer stuff:</h2>
            <p>I dont know what i am doing, this app does not collect any data, it is fully offline. I dont take any responisibility for what you do with this app, although i wouldnt know what illegal stuff you could do with what is basically a euphemism of a calculator. Please dont copy, publish, take credit, etc for this app. Just behave, ya nerds.<br>
            have fun :) <br>
            </p>
            <h2>PIN</h2>
        """.format(wynnpic.as_uri(), WAMCpic.as_uri()))

        layout.addWidget(help_text)