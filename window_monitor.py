import gtk
import wnck
import glib
import datetime

class WindowTitle(object):
    def __init__(self,filename):
        self.title = None
        self.time = datetime.datetime.now()
        glib.timeout_add(2000, self.record_activity) # Call get_title() every 2 seconds
        try:
            self.file = open(filename, 'ab')
        except IOError:
            pass

    def get_title(self):
        try:
            title = wnck.screen_get_default().get_active_window().get_name()
            #if self.title != title:
                #self.title  = title
            return title
        except AttributeError:
            return "TITLE ERROR"

    def get_catogery(self,title): # To be expanded later to add catogeries for each program
        return "Unknown"

    def record_activity(self):
        title = self.get_title()
        if self.title != title:
            self.title = title
            time_now = datetime.datetime.now()
            delta = time_now - self.time
            time_spent = ',' + str(delta.seconds) + '\n'
            self.file.write(time_spent)
            self.time = time_now
            catogery = self.get_catogery(title)
            record = [time_now.year, time_now.month, time_now.day, time_now.hour, time_now.minute, 
                    time_now.second, title , catogery]
            self.file.write(str.join(',', [str.replace(str(item), ',', '-') for item in record ]))
            self.file.flush()
        return True

WindowTitle("tmp.csv")
gtk.main()

