from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class BusSeat(models.Model):
    bus = models.ForeignKey('reservationsystem.bus', on_delete=models.CASCADE, editable=False)
    order = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(63)])

    row = models.CharField(max_length=1, editable=False)
    column = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], editable=False)

    @property
    def name(self):
        return f"{self.row}{self.column}"

    def __str__(self):
        return f"{self.bus.name} {self.name}"

    def save(self, *args, **kwargs):
        # execute only onCreate (when id is None)
        if not self.id:
            # automatically compute row and column of seat before saving
            row_size = 2
            self.row = chr(ord('A') + self.order // row_size)
            self.column = (self.order % row_size) + 1

        super(BusSeat, self).save(*args, **kwargs)
