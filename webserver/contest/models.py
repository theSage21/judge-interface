from socket import create_connection
from django.db import models


class Slave(models.Model):
    def __str__(self):
        return self.ip + str(self.port)

    ip = models.GenericIPAddressField()
    port = models.IntegerField()

    def is_alive(self):
        addr = (self.ip, self.port)
        try:
            con = create_connection(addr)
        except:
            return False
        else:
            con.sendall('Alive')
            if con.recv(512).decode() == 'True':
                return True
            else:
                return False

    def get_address(self):
        return (self.ip, self.port)
