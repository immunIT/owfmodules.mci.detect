import time

from octowire_framework.module.AModule import AModule
from octowire.mci import MCI


class Detect(AModule):
    def __init__(self, owf_config):
        super(Detect, self).__init__(owf_config)
        self.meta.update({
            'name': 'MCI detect interface',
            'version': '1.0.0',
            'description': 'Module to detect and print MCI interface information.',
            'author': 'Jordan Ovrè / Ghecko <jovre@immunit.ch>, Paul Duncan / Eresse <pduncan@immunit.ch>'
        })

    def detect(self):
        mci_interface = MCI(serial_instance=self.owf_serial)
        self.logger.handle("Trying to retrieve MCI interface information..", self.logger.INFO)
        iteration = 5
        while iteration > 0:
            resp = mci_interface.detect()
            if resp['status_str'] != "Initializing":
                if resp['status_str'] != "OK":
                    self.logger.handle("Failed to retrieved MCI interface information.", self.logger.ERROR)
                    level = self.logger.ERROR
                else:
                    self.logger.handle("Successfully retrieved MCI interface information.", self.logger.SUCCESS)
                    level = self.logger.RESULT
                self.logger.handle(f"Status: {resp['status_str']}", level)
                self.logger.handle(f"Memory type: {resp['type_str']}", level)
                self.logger.handle(f"Version: {resp['version_str']}", level)
                self.logger.handle(f"Capacity: {resp['capacity']} KB", level)
                return resp
            iteration = iteration - 1
        else:
            self.logger.handle("Unable to retrieve MCI interface information.", self.logger.ERROR)

    def run(self, return_value=False):
        """
        Main function.
        call detect function to try identifying MCI interface.
        :return: Nothing or dictionary if return_value is True.
        """
        # If detect_octowire is True then Detect and connect to the Octowire hardware. Else, connect to the Octowire
        # using the parameters that were configured. It sets the self.owf_serial variable if the hardware is found.
        self.connect()
        if not self.owf_serial:
            return
        try:
            mci_info = self.detect()
            if return_value:
                return mci_info
        except ValueError as err:
            self.logger.handle(err, self.logger.ERROR)
            if return_value:
                return None
        except Exception as err:
            self.logger.handle("{}: {}".format(type(err).__name__, err), self.logger.ERROR)
            if return_value:
                return None
