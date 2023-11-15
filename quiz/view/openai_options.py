import os
import requests
from dotenv import load_dotenv

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QDialog

from quiz.view.openai_options_ui import Ui_Openai_dlg

load_dotenv(os.environ["HOME"] + "/.chatgpt")

BASIC_URI = "https://api.openai.com/v1"
HEADERS = {"Authorization": "Bearer " + os.environ.get("OPENAI_API_KEY")}
COMPANY = "ZeroSubstance"
APPNAME = "FreeQuizApp"
# load_dotenv(os.environ["HOME"] + "/.chatgpt")
# openai.api_key = os.environ["OPENAI_API_KEY"]


def list_models(p=True):
    filter = "gpt"
    uri = BASIC_URI + "/models"
    response = requests.get(uri, headers=HEADERS)
    if response.status_code != 200:
        return {"error": response.status_code}
    response = response.json()
    engines = [x["id"] for x in response["data"] if filter in x["id"]]
    engines.sort()
    return engines


class Openai(QDialog, Ui_Openai_dlg):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("OpenAI Options")
        self.settings = QSettings(COMPANY, APPNAME)
        user_engine = self.settings.value("user_gpt_engine")
        def_engine = self.settings.value("default_gpt_engine")

        self.tokenEdit.editingFinished.connect(self.tokenChanged)
        self.openai_engine_cb.currentIndexChanged.connect(self.engineChanged)
        self.openai_close_pb.clicked.connect(self.close)

        engines = ["None"] + list_models()
        msg = (
            '<html><head/><body><p><span style="font-size:18pt; font-weight:700; color:#deddda;">'
            'Choose gpt engine </span></p><span style="color:#ffffff;">'
            "<p>Choose your own gpt engine if you like</p>"
        )
        chosen_engine = (
            user_engine if user_engine else def_engine if def_engine else "gpt-4"
        )
        if def_engine:
            msg += f'<p>"The default gpt engine is: <b>{def_engine}</b></p>'

        msg += "<p>Select None to opt out of the gpt API</p><hr></span></body></html>"

        self.choose_engine_lbl.setText(msg)
        self.openai_engine_cb.addItems(engines)
        self.openai_engine_cb.setCurrentIndex(engines.index(chosen_engine))

        # Populate the QComboBox openai_engine_cb with the list of engines

    def tokenChanged(self):
        # print("value", value)
        print("widget", self.tokenEdit.text())

    def engineChanged(self, index):
        value = self.openai_engine_cb.currentText()

        self.settings.setValue("user_gpt_engine", value)

    def close(self):
        super(Openai, self).close()


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    # print(list_models())

    app = QApplication([])
    dialog = Openai()
    dialog.show()
    app.exec()
