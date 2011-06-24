import gtk
import wnck
import glib
import time
import os
import sys


SCREENSHOTS_DIR = os.getenv("HOME") + "/Screenshots/"
LOGFILE = os.getenv("HOME") + "/activity.log"

print "SCREENSHOTS_DIR:", SCREENSHOTS_DIR
print "LOGFILE:", LOGFILE

class ActivityMonitor(object):
    def __init__(self,log_file, shots_dir):
        self.title = None
        self.quality = 50
        glib.timeout_add(2000, self.log_activity) # Call get_title() every 2 seconds
        try:
            self.log_file = open(log_file, 'ab')
            self.shots_dir = shots_dir
        except IOError: # Unable to create file exception
            pass
        except OSError: # Unable to create directory
            pass

    def get_title(self):
        try:
            title = wnck.screen_get_default().get_active_window().get_name()
            return title
        except AttributeError:
            return "TITLE ERROR"

    def get_screenshot(self):
        root_window = gtk.gdk.get_default_root_window()
        size = root_window.get_size()
        pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,
                False,
                8,
                size[0],
                size[1])
        return pixbuf.get_from_drawable(root_window,
                root_window.get_colormap(),
                0, 0, 0, 0,
                size[0],
                size[1])

    def get_catogery(self,title): # To be expanded later to add catogeries
        return "Unknown"

    def log_activity(self):
        title = self.get_title()

        if self.title != title:
            activity_time = time.localtime()
            self.title = title
            self.log_file.write("%s,%s,%s\n" % (time.strftime("%Y-%m-%d %H:%M:%S", activity_time), title, self.get_catogery(title) ) )
            self.log_file.flush()

            screenshot = self.get_screenshot()
            path = time.strftime("%Y/%m/%d", activity_time)
            fullpath = os.path.join(self.shots_dir, path)

            filename = "%s.png" % time.strftime("%H%M%S", activity_time)

            if not os.path.exists(fullpath):
                os.makedirs(fullpath)
            screenshot.save(os.path.join(fullpath, filename), "png" )

        return True

if __name__ == '__main__':
    if len(sys.argv) == 3:
        ActivityMonitor(sys.argv[1], sys.argv[2])
    else:
        ActivityMonitor(LOGFILE, SCREENSHOTS_DIR)
    gtk.main()

