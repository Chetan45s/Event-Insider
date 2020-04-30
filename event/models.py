from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.core.validators import MinValueValidator, RegexValidator
from PIL import Image
from django.utils.timezone import now

# Create your models here.
class club(models.Model):
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=500)
    president = models.ForeignKey(to=User,on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(default='clubdefault.jpg',upload_to="club_images\\")
    mail = models.EmailField(max_length=254)
    phone_number = models.CharField(validators = [RegexValidator("^0?[5-9]{1}\d{9}$")], max_length=10, null = True, blank = True, unique = True)
    insta = models.URLField(max_length=200, null = True, blank = True)
    def __str__(self):
        return self.name
    
class post_event(models.Model):
    title = models.CharField(max_length=2000)
    date_posted = models.DateTimeField(auto_now_add=True)
    event_date = models.DateTimeField()
    description = models.TextField()
    register = models.ManyToManyField(User,related_name='event_registration',blank = True)
    image = models.ImageField(default='defaultpost.jpg',upload_to="event_images\\")
    author = models.ForeignKey(to = club,on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    def total_registrations(self):
        return self.register.count()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    First_Name = models.CharField(default = "First Name",max_length=50)
    Last_Name = models.CharField(default = "Last Name",max_length=50)
    School = models.CharField(default = "SCHOOL OF HUMANITIES AND ENGINEERING SCIENCES",choices = (("SCHOOL OF COMPUTER ENGINEERING & TECHNOLOGY","SCHOOL OF COMPUTER ENGINEERING & TECHNOLOGY"), 
                                                          ("SCHOOL OF ELECTRICAL ENGINNERING","SCHOOL OF ELECTRICAL ENGINNERING"),
                                                          ("SCHOOL OF MECHANICAL & CIVIL ENGINEERING","SCHOOL OF MECHANICAL & CIVIL ENGINEERING"),
                                                          ("SCHOOL OF CHEMICAL ENGINEERING","SCHOOL OF CHEMICAL ENGINEERING"),
                                                          ("SCHOOL OF HUMANITIES AND ENGINEERING SCIENCES","SCHOOL OF HUMANITIES AND ENGINEERING SCIENCES")), 
                                                                max_length=50)
    Roll_No = models.CharField(default = "ABC120",max_length=10)
    Year = models.CharField(default = "First Year", choices = (("First Year","First Year"), 
                                                               ("Second Year","Second Year"),
                                                               ("Third Year","Third Year"),
                                                               ("Final Year","Final Year")), 
                                                               max_length=50)
    club_joined = models.ForeignKey(to=club, on_delete=models.CASCADE, null = True, blank = True)    
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')



    def __str__(self):
        return self.user.username
        
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.img.path)
    
class BlogComment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(post_event, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE,blank= True, null = True)
    reply = models.ForeignKey("self", related_name="replies",null=True,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default = now)

    def __str__(self):
        return self.comment

class RegistrationForEvent(models.Model):
    event_title = models.ForeignKey(post_event, on_delete=models.CASCADE) 
    First_Name = models.CharField(max_length=50)
    Last_Name = models.CharField(max_length=50)
    School = models.CharField(max_length = 50), 
    Roll_No = models.CharField(max_length=10)
    Year = models.CharField(max_length=50)
    timestamp = models.DateTimeField(default = now)
       