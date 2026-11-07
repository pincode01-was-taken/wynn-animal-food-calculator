import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QSpinBox, QComboBox, QDialog, QTextBrowser)
import IngredTable
from scipy.optimize import milp, Bounds, LinearConstraint
import numpy as np
from help_window import HelpWindow



onlyLvl1Ingreds = True

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configure main window
        self.setWindowTitle("WAFC")
        self.resize(1000, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        layout = QVBoxLayout(central_widget)

        # settings buttons
        button_layout = QHBoxLayout()


        newMount = QPushButton("Set to new mount")
        dropdown = QComboBox()

        dropdown.addItem("Only lvl 1 ingreds")
        dropdown.addItem("highest possible ingreds")


        newMount.clicked.connect(self.newMount_clicked)

        dropdown.currentTextChanged.connect(self.mode_changed)
        selected_mode = dropdown.currentText()
        dropdown.currentIndexChanged.connect(self.update_table)
        
        button_layout.addWidget(newMount)
        button_layout.addWidget(dropdown)



        layout.addLayout(button_layout)

        help_button = QPushButton("Help")
        layout.addWidget(help_button)
        help_button.clicked.connect(self.open_help)

        # Create table
        self.table = QTableWidget(2, 8)

        # column headers
        self.table.setHorizontalHeaderLabels(
            ["Speed", "Acceleration", "Altitude", "Energy", "Handling", "Toughness", "Boost", "Training"]
        )
        self.table.setVerticalHeaderLabels(["current value","max potential"])

        # Add table to layout
        layout.addWidget(self.table)


        for row in range(2):
            for column in range (8):
                spin_box = QSpinBox()
                spin_box.setRange(0, 500)
                self.table.setCellWidget(row, column, spin_box)

        # calculation button
        self.calculate_button = QPushButton("Go")
        layout.addWidget(self.calculate_button)

        # Explanation txt
        self.result_label = QLabel("Enter your mounts current max in the first row and the absolut max in the second row; then click 'go'")
        self.result_label.setWordWrap(True)
        layout.addWidget(self.result_label)
        

        # Connect button to calculation function
        self.calculate_button.clicked.connect(self.calculate)

        
    def mode_changed(self, selected_mode):
        if selected_mode == "Only lvl 1 ingreds":
            onlyLvl1Ingreds = True

        if selected_mode == "highest possible ingreds":
            onlyLvl1Ingreds = False

        print("onlyLvl1Ingreds:", onlyLvl1Ingreds)
        

    def open_help(self):
        help_window = HelpWindow(self)
        help_window.exec()

    def update_table(self, selected_mode):
        if selected_mode:
            self.table.insertRow(0)
            self.table.setVerticalHeaderLabels(["training level", "current value","max potential"])
            for column in range (8):
                spin_box = QSpinBox()
                spin_box.setRange(0, 500)
                self.table.setCellWidget(0, column, spin_box)

        elif not selected_mode and self.table.rowCount()>2:
            self.table.removeRow(0)

        else:
            print("ERROR updating table")


    def newMount_clicked(self):
        print("button has been pressed")
        row = self.table.rowCount()-1
        print(row)
        for column in range(8):
            item = self.table.cellWidget(row, column)

            if item is not None:
                item.setValue(30)

        row2 = row - 1
        for column in range(8):
            item2 = self.table.cellWidget(row2, column)

            if item2 is not None:
                item2.setValue(10)

    def calculate(self):
        # Read the values
        if self.table.rowCount() == 2:
            a = 0
        elif self.table.rowCount() == 3:
            a = 1
        else:
            print("ERROR counting rows")


        currSpeed = self.table.cellWidget(0+a, 0).value()
        currAcc = self.table.cellWidget(0+a, 1).value()
        currAlt = self.table.cellWidget(0+a, 2).value()
        currEnergy = self.table.cellWidget(0+a, 3).value()
        currHandl = self.table.cellWidget(0+a, 4).value()
        currTough = self.table.cellWidget(0+a, 5).value()
        currBoost = self.table.cellWidget(0+a, 6).value()
        currTrain = self.table.cellWidget(0+a, 7).value()
        maxSpeed = self.table.cellWidget(1+a, 0).value()
        maxAcc = self.table.cellWidget(1+a, 1).value()
        maxAlt = self.table.cellWidget(1+a, 2).value()
        maxEnergy = self.table.cellWidget(1+a, 3).value()
        maxHandl = self.table.cellWidget(1+a, 4).value()
        maxTough = self.table.cellWidget(1+a, 5).value()
        maxBoost = self.table.cellWidget(1+a, 6).value()
        maxTrain = self.table.cellWidget(1+a, 7).value()

        # tuples to store max and curr values
        curr = {"Speed": currSpeed, "Acceleration": currAcc, "Altitude": currAlt, "Energy": currEnergy, "Handling": currHandl, "Toughness": currTough, "Boost": currBoost, "Training": currTrain}
        maxVal = {"Speed": maxSpeed, "Acceleration": maxAcc, "Altitude": maxAlt, "Energy": maxEnergy, "Handling": maxHandl, "Toughness": maxTough, "Boost": maxBoost, "Training": maxTrain}
        diff = {"Speed": max(0, (maxSpeed - currSpeed)),
                "Acceleration": max(0, (maxAcc - currAcc)),
                "Altitude": max(0, (maxAlt - currAlt)),
                "Energy": max(0, (maxEnergy - currEnergy)),
                "Handling": max(0, (maxHandl - currHandl)),
                "Toughness": max(0, (maxTough - currTough)),
                "Boost": max(0, (maxBoost - currBoost)),
                "Training": max(0, (maxTrain - currTrain))}
        if a == 1:
            trainingSpeed = self.table.cellWidget(0, 0).value()
            trainingAcc = self.table.cellWidget(0, 1).value()
            trainingAlt = self.table.cellWidget(0, 2).value()
            trainingEnergy = self.table.cellWidget(0, 3).value()
            trainingHandl = self.table.cellWidget(0, 4).value()
            trainingTough = self.table.cellWidget(0, 5).value()
            trainingBoost = self.table.cellWidget(0, 6).value()
            trainingTrain = self.table.cellWidget(0, 7).value()

            train = {"Speed": trainingSpeed, "Acceleration": trainingAcc, "Altitude": trainingAlt, "Energy": trainingEnergy, "Handling": trainingHandl, "Toughness": trainingTough, "Boost": trainingBoost, "Training": trainingTrain}
            trainMax = (trainingSpeed, trainingAcc, trainingAlt, trainingEnergy, trainingHandl, trainingTough,trainingBoost, trainingTrain)
        elif a == 0:
            trainMax = (1,1,1,1,1,1,1,1)
        else:
            print("Error creating 'train'")

        trainLvl = int(max(trainMax))
        if trainLvl < 105:
            trainMaxLvl = (trainLvl //10)*10
        elif trainLvl < 110:
            trainMaxLvl = 105
        elif trainLvl < 115:
            trainMaxLvl = 110
        else:
            trainMaxLvl = 115

        if trainMaxLvl <= 1:
            trainMaxLvl = 1

        ingred_table = IngredTable.lvl_tables[trainMaxLvl]
        ingred_names = IngredTable.inlvl_tables[trainMaxLvl]
        print(diff)

        ingredients = ingred_table["MAT"]
        number_of_ingreds = len(ingredients)

        stats = [
            "Speed", "Acceleration", "Altitude", "Energy",
            "Handling", "Toughness", "Boost", "Training"
        ]

        # Build the contribution matrix
        contributions = [
            ingred_table[stat]
            for stat in stats
        ]

        # Minimize the total number of ingredients
        objective = [1] * number_of_ingreds

        # Each ingredient quantity must be a non-negative integer
        bounds = Bounds(
            lb=[0] * number_of_ingreds,
            ub=[np.inf] * number_of_ingreds
        )

        # Required contribution for each stat
        required = [diff[stat] for stat in stats]

        constraints = LinearConstraint(
            contributions,
            lb=required,
            ub=[np.inf] * len(stats)
        )

        # Solve
        result = milp(
            c=objective,
            integrality=[1] * number_of_ingreds,
            bounds=bounds,
            constraints=constraints
        )

        if result.success:
            for i, quantity in enumerate(result.x):
                quantity = round(quantity)

                if quantity > 0:
                    print(f"{ingredients[i]}: {quantity}")

            print(f"Total ingredients: {round(result.fun)}")

        else:
            print("No valid solution found:", result.message)


        if result.success:
            solution = []

            for i, quantity in enumerate(result.x):
                quantity = round(quantity)

                if quantity > 0:
                    solution.append(
                        f"{ingred_names[int(np.floor(i/2))]} {ingredients[i]}: {quantity}"
                    )
                    #print(solution)
            total = round(result.fun)

            if solution:
                message = (
                    "Recommended ingredients:\n"
                    + "\n".join(solution)
                    + f"\n\nTotal ingredients: {total}"
                )
            else:
                message = "No ingredients needed! All stats already meet their targets."

            self.result_label.setText(message)

        else:
            self.result_label.setText(
                f"No valid solution found.\n{result.message}"
            )
        #print(diff, ingredients, number_of_ingreds)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

# hopefully i will never have to update/revisit any of this mess o.o

# so much for that, fuck
# to do
# 
# help window explaining all imputs and where to find them
# help window on how mounts  work at all
# reset button - naaaahhhhh, new mount works for this, dont clutter UI
# button for ingreds already q'ed - maybe later cuz when input you can just see in the ingredslist
# farming locations - i am too lazy, and this would be a lot of work (and requiring somewhat frequent updates)