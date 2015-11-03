from socket import create_connection
from django.db import models
from django.utils import timezone


class Slave(models.Model):
    def __str__(self):
        return self.ip + str(self.port)

    ip = models.GenericIPAddressField()
    port = models.IntegerField()
    busy = models.BooleanField(default=False)

    def is_alive(self):
        addr = (self.ip, self.port)
        try:
            con = create_connection(addr)
        except:
            return False
        else:
            con.sendall('Alive'.encode('utf-8'))
            return True

    def get_address(self):
        return (self.ip, self.port)

    def __enter__(self):
        self.busy = True
        self.save()

    def __exit__(self, exc_type, exc_value, traceback):
        self.busy = False
        self.save()


class ContestControl(models.Model):
    "Control for the contest"
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100, default='Contest')
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now)
