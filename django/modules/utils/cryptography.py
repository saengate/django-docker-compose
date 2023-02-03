import base64
import os
import random
import string

from Crypto.Cipher import AES


class Cryptography(object):

    def __init__(self, rge=16, iv_random=True, altchars=None):
        self.rge = rge
        self.key = ''.join(
            random.choice(
                string.ascii_uppercase + string.digits,
            ) for x in range(self.rge)
        )

        # Initialization vector. It has the first 16 bytes in the message.
        # it is used to have the same message encrypted but with different
        # result CBCMode de AES
        if iv_random:
            self.iv = os.urandom(self.rge * 1024)[0:self.rge]
        else:
            # This case should be for the emails
            self.iv = ' ' * self.rge

        # The information of the message have to be multiple of 16
        # (AES block size), for this reason PADDING.
        # PADDING Guarantees that the message is multiple of the block
        self.padding = ' '
        self.pad = lambda s: s + (self.rge - len(s) % self.rge) * self.padding
        self.altchars = altchars

    def encrypt(self, value):
        return base64.b64encode(
            self.iv + AES.new(
                self.key, AES.MODE_CBC, self.iv,
            ).encrypt(self.pad(value)),
            altchars=self.altchars,
        )

    def decrypt(self, value, key, base_encode='utf-8'):
        return AES.new(
            key, AES.MODE_CBC, value[:self.rge],
        ).decrypt(
            base64.b64decode(value, altchars=self.altchars),
        )[self.rge:].decode(base_encode).rstrip(self.padding)
