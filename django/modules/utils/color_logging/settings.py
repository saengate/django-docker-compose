# -*- coding: utf-8 -*-
try:
    from termcolor import colored
except ImportError:
    raise AssertionError('Necesitas instalar la libreria termcolor.')
# log level detail

# %(name)s            Name of the logger(logging channel)
# %(levelno)s         Numeric logging level for the message(DEBUG, INFO,
#                                                             WARNING, ERROR, CRITICAL)
# %(levelname)s       Text logging level for the message("DEBUG", "INFO",
#                                                         "WARNING", "ERROR", "CRITICAL")
# %(pathname)s        Full pathname of the source file where the logging
#                     call was issued(if available)
# %(filename)s        Filename portion of pathname
# %(module)s          Module(name portion of filename)
# %(lineno)d          Source line number where the logging call was issued
#                     (if available)
# %(funcName)s        Function name
# %(created)f         Time when the LogRecord was created(time.time()
#                                                         return value)
# %(asctime)s         Textual time when the LogRecord was created
# %(msecs)d           Millisecond portion of the creation time
# %(relativeCreated)d Time in milliseconds when the LogRecord was created,
#                     relative to the time the logging module was loaded
#                     (typically at application startup time)
# %(thread)d          Thread ID(if available)
# %(threadName)s      Thread name(if available)
# %(process)d         Process ID(if available)
# %(message)s         The result of record.getMessage(), computed just as
#                     the record is emitted

# See detail in log in the order if is True
details = dict(
    gname=[False, 0, '%(name)s'],
    glevelno=[False, 0, '%(levelno)s'],
    glevelname=[True, 2, '%(levelname)s'],
    gpathname=[False, 0, '%(pathname)s'],
    gfilename=[False, 0, '%(filename)s'],
    gmodule=[True, 3, '[%(module)s]'],
    glineno=[False, 0, '%(lineno)d'],
    gfuncName=[True, 4, colored('[%(funcName)s]\n', 'cyan')],
    gcreated=[False, 0, '%(created)f'],
    gasctime=[True, 1, '%(asctime)s'],
    gmsecs=[False, 0, '%(msecs)d'],
    grelativeCreated=[False, 0, '%(relativeCreated)d'],
    gthread=[False, 0, '%(thread)d'],
    gthreadName=[False, 0, '%(threadName)s'],
    gprocess=[False, 0, '%(process)d'],
    gmessage=[True, 5, '%(message)s'],
)

delimit = ' - '

# Si deseas modificar las configuraciones por defecto, crea un archivo
# local_settings.py y sobreescribe las variables allí.
# este se importara desde aquí y sustituirá los valores al ser llamado por
# el color_logging.

try:
    from local_settings import *  # NOQA
except ImportError:
    pass
