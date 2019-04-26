import logging
import time

timestr = time.strftime("%Y%m%d-%H%M%S")

log_filename = 'Logs/'+ timestr + '_app.log'

def logSettings():
    logging.basicConfig(filename=log_filename, filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)
    
def logException(e:Exception):
    logging.exception(str(e))

def logInfo(message):
    logging.info(message)