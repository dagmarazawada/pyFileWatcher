#!/usr/bin/python

import sys, os, platform, getopt
import shutil, logging
import datetime, time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

today = datetime.date.today()

### DEFINE start

# root dir (place this script in it)
win_rootdir = "C:\\___d___\\_python\\pyfilewatcher\\"
lin_rootdir = "/home/d/python/pyfilewatcher/"
# folder to be watched
win_dir_to_watch = "C:\\test\\watchme\\"
lin_dir_to_watch = "/home/d/watchme/"
# copy destination
win_new_destination = "C:\\test\\NEW_DEST\\"
lin_new_destination = "/home/d/NEW_DEST/"

### DEFINE end

### python3 watchdog.py -r <rootdir> -d <dir_to_watch> -n <new destination>



class Watcher:
    
    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, dir_to_watch, recursive=True)
        self.observer.start()
        logging.info('watchdog started')
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("watchdog stopped")
            logging.info('watchdog stopped')

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            #print("Received dir event - %s." % event.src_path)
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            try:
                print(today.strftime('%Y-%m-%d %I:%M:%S %p') + " - created - %s" % event.src_path)
            except:
                pass
            logging.info('new item created: %s ' % event.src_path)
            inthedir = separator.join(event.src_path.split(separator)[1:-1])
            Helper.copy_all(event.src_path , new_destination + inthedir)
            logging.info(event.src_path + ' copied to: ' + new_destination + inthedir)


        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            try:
                print(today.strftime('%Y-%m-%d %I:%M:%S %p') + " - modified - %s" % event.src_path)
            except:
                pass
            logging.info('item modified: %s ' % event.src_path)
            inthedir = separator.join(event.src_path.split(separator)[1:-1])
            Helper.copy_all(event.src_path , new_destination + inthedir)
            logging.info(event.src_path + ' copied to: ' + new_destination + inthedir)

        elif event.event_type == 'deleted':
            # Taken any action here when a file is deleted.
            try:
                print(today.strftime('%Y-%m-%d %I:%M:%S %p') + " - deleted - %s" % event.src_path)
            except:
                pass
            logging.info('item deleted from watched dir: %s' % event.src_path)

class Helper:

    def main(self, argv):
        global rootdir, new_destination, separator, dir_to_watch
        h.script_info()
        try:
            opts, args = getopt.getopt(argv,"hr:d:n:",["rootdir=","dir-to-watch=","new-destination="])
        except getopt.GetoptError:
            h.script_info()
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                h.script_info()
                #sys.exit()
            elif opt in ("-r", "--rootdir"):
                rootdir = arg + separator
            elif opt in ("-d", "--dir-to-watch"):
                dir_to_watch = arg + separator
            elif opt in ("-n", "--new-destination"):
                new_destination = arg + separator
        print ('rootdir: ', rootdir)
        print ('dir to watch: ', dir_to_watch)
        print ('new destination: ', new_destination)

        return rootdir, dir_to_watch, new_destination

    def script_info(self):
        print('')
        print('*** WATCHDOG.PY ***')
        print ('-- USAGE: watchdog.py [-r <rootdir>] [-d <dir_to_watch>] [-n <new_destination>]')
        print('   // for dirs provide absolute path, no quotation marks')
        print('-- if arguments not specified - defaults from script taken')
        print('')

    def check_os(self):
        global rootdir, new_destination, separator, dir_to_watch

        # define separator for different os:
        win_sep = "\\"
        lin_sep = "/"

        if platform.system() == "Windows":
            rootdir = win_rootdir
            separator = win_sep   
            dir_to_watch = win_dir_to_watch + separator
            new_destination = win_new_destination + separator
        elif platform.system() == "Linux":
            rootdir = lin_rootdir
            separator = lin_sep
            dir_to_watch = lin_dir_to_watch + separator
            new_destination = lin_new_destination + separator
        else:
            print("Your system was not detected. You have to specify folder paths in scripts.")
        return rootdir, new_destination, separator, dir_to_watch

    def check_py_ver(self):
        req_version = (3,4)
        cur_version = sys.version_info

        if cur_version <= req_version:
           print("Your Python interpreter is " + platform.python_version() + " on which this script may not run properly. Please upgrade to 3.4 or run this script with: 'python3 watchdog.py'.")
           sys.exit(2)

    def copy_all(src, dst):
        try:
            if not os.path.exists(dst):
                os.makedirs(dst)
            if os.path.isdir(src):
                for item in os.listdir(src):
                    s = os.path.join(src, item)
                    d = os.path.join(dst, item)
                    if os.path.isdir(s):
                        copy_all(s, d)
                    else:
                        if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                            shutil.copy2(s, d)
            else:
                shutil.copy2(src, dst)
        except:
            pass


if __name__ == '__main__':
    h = Helper()
    h.check_os()
    h.check_py_ver()
    h.main(sys.argv[1:])
    w = Watcher()
    logging.basicConfig(filename='watched.log', format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.INFO)
    w.run()


'''

windows os probably raises few notices on creating/modifying files 
so overriting in dst folder is necessary to avoid files redundancy
uploader just have to upload to new catalogs in src


linux doesn't raise on_delete event
linux raises some other event on modifying in place
so FILE SHOULDN'T BE MODYFIED IN PLACE
copying new, overriting is ok


different file names, coding, russian etc - ok
but
russian coding throws exception in windows console (it depends on console coding so 
there is exception pass for it)


'''
