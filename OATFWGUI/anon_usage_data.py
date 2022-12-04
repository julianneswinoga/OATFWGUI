import logging
import hashlib
import subprocess
import json
from pathlib import Path

from PySide6.QtWidgets import QDialog, QDialogButtonBox, QPlainTextEdit, QVBoxLayout, QLabel
from PySide6.QtGui import QFont
import pygments
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter

from platform_check import get_platform, PlatformEnum
from gui_state import LogicState

log = logging.getLogger('')


class AnonStatsDialog(QDialog):
    def __init__(self, logic_state: LogicState, parent=None):
        super().__init__(parent)

        self.setWindowTitle('What statistics will be uploaded?')

        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        usage_stats_html = dict_to_html(create_anon_stats(logic_state))

        wLbl_1 = QLabel('''
These statistics are invaluable for us developers on figuring out what our users are actually
building, so we can figure out where to put our (limited!) time working towards improving.
After a successful OAT firmware upload the following data will be sent to our statistics server:
'''.replace('\n', ' '))
        wLbl_1.setWordWrap(True)

        wTxt_html = QPlainTextEdit()
        wTxt_html.setReadOnly(True)
        wTxt_html.appendHtml(f'{usage_stats_html}')

        wLbl_2 = QLabel('''
(the data might not fully be populated yet, you need to progress through the GUI steps first)
'''.replace('\n', ' '))
        italic_font = QFont()
        italic_font.setItalic(True)
        wLbl_2.setFont(italic_font)
        wLbl_2.setWordWrap(True)

        wLbl_3 = QLabel('''
Additionally your IP address may be logged for rough geo-location purposes.
'''.replace('\n', ' '))
        wLbl_3.setWordWrap(True)

        self.layout = QVBoxLayout()
        self.layout.addWidget(wLbl_1)
        self.layout.addWidget(wTxt_html)
        self.layout.addWidget(wLbl_2)
        self.layout.addWidget(wLbl_3)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


def dict_to_html(in_dict: dict) -> str:
    json_str = json.dumps(in_dict, indent=4, sort_keys=True)
    json_lexer = JsonLexer()
    html_formatter = HtmlFormatter(noclasses=True, nobackground=True)
    data_html = pygments.highlight(json_str, json_lexer, html_formatter)
    return data_html


def create_anon_stats(logic_state: LogicState) -> dict:
    if logic_state.release_idx is not None:
        release_name = logic_state.release_list[logic_state.release_idx].nice_name
    else:
        release_name = None

    if logic_state.config_file_path is not None:
        with open(Path(logic_state.config_file_path).resolve(), 'r') as fp:
            config_file = fp.read()
    else:
        config_file = None

    stats = {
        'uuid': get_uuid(),
        'pio_env': logic_state.pio_env,
        'release_version': release_name,
        'config_file': config_file,
    }
    return stats


def upload_anon_stats(anon_stats: dict) -> bool:
    log.info('Uploading statistics')

    return False


def get_uuid() -> str:
    machine_id_fn = {
        PlatformEnum.WINDOWS: get_uuid_windows,
        PlatformEnum.LINUX: get_uuid_linux,
        PlatformEnum.UNKNOWN: lambda: 'unknown',
    }.get(get_platform())
    machine_id_str = machine_id_fn()

    if 'unknown' in machine_id_str.lower():
        uuid_str = machine_id_str  # Keep as human-readable, don't hash
    else:
        uuid_str = hashlib.sha256(machine_id_str.encode()).hexdigest()
    log.debug(f'Got UUID {repr(uuid_str)}')
    return uuid_str


def get_uuid_windows() -> str:
    sub_proc = subprocess.run(
        ['powershell',
         '-Command',
         '(Get-CimInstance -Class Win32_ComputerSystemProduct).UUID',
         ],
        capture_output=True)
    if sub_proc.returncode != 0:
        return 'unknown-windows'
    windows_uuid = sub_proc.stdout.decode('UTF-8')
    return windows_uuid


def get_uuid_linux() -> str:
    id_file = Path('/etc/machine-id')
    if not id_file.exists():
        return 'unknown-linux'

    with open(id_file, 'r') as f:
        machine_id_contents = f.read().strip()
    return machine_id_contents
