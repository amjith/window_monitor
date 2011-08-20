#!/usr/bin/python
from datetime import datetime
import os
import sys

import glib
import gtk
import wnck
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Unicode, DateTime

Base = declarative_base()

class ActivityRecord(Base):
    __tablename__ = 'activity_records'

    time = Column(DateTime, primary_key=True)
    title = Column(Unicode)
    category = Column(String)

    def __init__(self, time, title, category):
        self.time = time
        self.title = title
        self.category = category

    def __repr__(self):
        return "<ActivityRecord('%s', '%u', '%s')>" % (self.time,
                                                       self.title,
                                                       self.category)

SCREENSHOTS_DIR = os.getenv("HOME") + "/Screen-shots/"
LOGFILE = os.getenv("HOME") + "/activity.log"
DATABASE_URL = 'sqlite:///test.db'

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

        self.engine = create_engine(DATABASE_URL, echo=True)
        Session = sessionmaker(bind=self.engine)

        self.session = Session()
        Base.metadata.create_all(self.engine)


    def get_title(self):
        try:
            title = wnck.screen_get_default().get_active_window().get_name()
            return unicode(title)
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

    # To be expanded later to add categories
    def get_category(self,title):
        return "Unknown"

    def log_activity(self):
        title = self.get_title()

        if self.title != title:
            activity_time = datetime.now()
            self.title = title
            print type(self.title)
            activity_record = ActivityRecord(activity_time,
                                             title,
                                             "Not Working")
            self.session.add(activity_record)
            self.session.commit()

            screenshot = self.get_screenshot()
            path = "%d/%d/%d" % (activity_time.year,
                                 activity_time.month,
                                 activity_time.day)
            fullpath = os.path.join(self.shots_dir, path)

            filename = "%d%d%d.png" % (activity_time.hour,
                                       activity_time.minute,
                                       activity_time.second)

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

