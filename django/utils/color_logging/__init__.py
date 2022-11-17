# -*- coding: utf-8 -*-
"""
https://pypi.org/project/termcolor/

Monitore de archivos logs con identificación de colores.

Como usar:

    from utils.color_logging import logger

    def hacer_algo():
        logger.info('Algo de info')
        logger.error('Oh! un error')
        logger.warning('Falsa alarma!')
        logger.critical('Se murio!')

Creado por Saúl Galán
Fecha: 26-04-2019
"""
import logging

from utils.color_logging.settings import (
    details,
    delimit,
)

try:
    from termcolor import colored
except ImportError:
    raise AssertionError('Necesitas instalar la libreria termcolor.')

logging.basicConfig()


class NewLogger(logging.Logger):

    def __init__(self, name=None):
        super(NewLogger, self).__init__(name)

    def _log(self, level, msg, args, exc_info=None, extra=None):
        nlevel = logging.getLevelName(level)
        color = 'on_grey'
        if nlevel == 'CRITICAL' or nlevel == 'FATAL':
            color = 'magenta'
        elif nlevel == 'ERROR':
            color = 'red'
            exc_info = True
        elif nlevel == 'EXCEPTION':
            color = 'blue'
        elif nlevel == 'WARNING' or nlevel == 'WARN':
            color = 'yellow'
        elif nlevel == 'INFO':
            color = 'green'
        elif nlevel == 'DEBUG':
            color = 'blue'
            exc_info = True

        msg = colored(msg, color)
        super(NewLogger, self)._log(
            level,
            msg, args,
            exc_info,
            extra,
        )


def formatter():

    try:
        dett = {k: v for k, v in details.items() if v[0] is True}
        dets = sorted(dett.items(), key=lambda kv: (kv[1][1], kv[0]))
    except IndexError:
        raise AssertionError(
            'Los valores del details en setting son correctos.')

    lstr = ''
    i = 0
    for orden in dets:
        if i > 0:
            lstr += delimit
        try:
            lstr += orden[1][2]
        except IndexError:
            raise AssertionError('Los valores del details en setting son correctos.')
        i += 1

    log_format = (lstr)

    return log_format
