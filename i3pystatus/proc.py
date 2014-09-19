import psutil
import subprocess

from i3pystatus import IntervalModule


class Proc(IntervalModule):
    """
    TODO: Write documentation
    """

    settings = (
        ("format", "Formatting to use (defaults to {procname})"),
        ("format_down", "Formatting when the process is down (defaults to {procname})"),
        ("procname", "Name of the process when it is not running (required)"),
        ("proccmd", "Command to start the process when clicking the Module"),
        ("color_up", "Color when the proc is running (defaults to #00FF00)"),
        ("color_down", "Color when the proc is not running (defaults to #FF0000"),
    )
    required = ("procname",)
    format = "{procname}: yes"
    format_down = "{procname}: no"
    proccmd = ['/usr/local/nc/ncsvc', '-h', 'uvavpn.uva.nl', '-u', '10542590', '-p', 'Miqis147', '-r', 'users', '-f', '/usr/local/nc/certificaat-uvavpn.der']
    color_up = "#00FF00"
    color_down= "#FF0000"

    def run(self):

        # Find the processname in the process list, if found set color to up
        self.tracking_proc = None
        proc_color = self.color_down
        for proc in psutil.process_iter():
            if (proc.name() == self.procname):
                self.tracking_proc = proc
                self.proccmd = self.tracking_proc.cmdline()

        cdict = {
            "procname": self.procname,
            "procpid": self.tracking_proc.pid if self.tracking_proc else "",
            "procppid": self.tracking_proc.ppid() if self.tracking_proc else "",
            "procexe": self.tracking_proc.exe() if self.tracking_proc else "",
            "proccmd": self.proccmd,
            "procstatus": self.tracking_proc.status() if self.tracking_proc else "",
        }

        self.output = {
            "full_text": self.format.format(**cdict) if self.tracking_proc else self.format_down.format(**cdict),
            "color": self.color_up if self.tracking_proc else self.color_down
        }
    def on_leftclick(self):
        """
        TODO: Fix kill()
        """
        if (self.tracking_proc):
            self.tracking_proc.kill()
            self.tracking_proc = None
        else:
            subprocess.call(self.proccmd)
