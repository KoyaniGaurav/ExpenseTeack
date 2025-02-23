from django.db import models
from django.contrib.auth.hashers import make_password,check_password


class UserReg(models.Model):
    userId = models.AutoField(primary_key=True)  # Auto-incremented ID
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Store hashed password

    def save(self, *args, **kwargs):
        """Hash the password before saving."""
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        """Check if a raw password matches the stored hashed password."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name
    
class Expence(models.Model):
    userId = models.ForeignKey(UserReg, on_delete=models.CASCADE)
    expance_name = models.CharField(max_length=100,default="")
    category = models.CharField(max_length=100,default="")
    cost = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.category