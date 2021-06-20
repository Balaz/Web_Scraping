import logging

logging.basicConfig(filename='debug.log',
                    level=logging.DEBUG,
                    filemode='w',
                    format='[ %(levelname)-8s ] %(asctime)s - %(filename)-20s ' +
                           '{ %(funcName)23s(): %(lineno)-3s >> %(message)s',
                    datefmt='%H:%M:%S')
