# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from .scc_32u_controller import Scc32uController

class Scc32uPlugin(octoprint.plugin.StartupPlugin,
                   octoprint.plugin.TemplatePlugin,
                   octoprint.plugin.AssetPlugin,
                   octoprint.plugin.SimpleApiPlugin,
                   octoprint.plugin.SettingsPlugin):

    def __init__(self):
        self.controller = None

    def on_after_startup(self):
        port = self._settings.get(["port"])
        self.controller = Scc32uController(port)
        self._logger.info("SCC-32U Plugin started with port: {}".format(port))

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False),
            dict(type="tab", name="SCC-32U Control", custom_bindings=True)
        ]


    def get_assets(self):
        return {
            "js": ["js/SCC_32U.js"],
            "css": ["css/SCC_32U.css"],
            "less": ["less/SCC_32U.less"]
        }

    def get_api_commands(self):
        return dict(
            move=["servo_id", "angle"]
        )

    def on_api_command(self, command, data):
        if command == "move":
            servo_id = int(data.get("servo_id", 0))
            angle = int(data.get("angle", 1500))
            self._logger.info(f"Received move command for servo {servo_id} with angle: {angle}")
            self.controller.move_arm(servo_id, angle)
            return dict(status="success")

    def on_shutdown(self):
        self.controller.close()

    def get_settings_defaults(self):
        return {
            "port": ""
        }

    def get_update_information(self):
        return {
            "SCC_32U": {
                "displayName": "SCC-32U Plugin",
                "displayVersion": self._plugin_version,
                "type": "github_release",
                "user": "KobiSteve07",
                "repo": "OctoPrint-Scc_32u",
                "current": self._plugin_version,
                "pip": "https://github.com/KobiSteve07/OctoPrint-Scc_32u/archive/{target_version}.zip"
            }
        }

__plugin_name__ = "SCC-32U Plugin"
__plugin_version__ = "0.1.0"
__plugin_description__ = "Control the SCC-32U robot arm from OctoPrint"
__plugin_author__ = "Tyler Kobida"
__plugin_author_email__ = "dtkobida@gmail.com"
__plugin_url__ = "https://github.com/KobiSteve07/OctoPrint-Scc_32u"
__plugin_license__ = "AGPLv3"
__plugin_pythoncompat__ = ">=3,<4"  # Ensure Python 3 compatibility

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Scc32uPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }