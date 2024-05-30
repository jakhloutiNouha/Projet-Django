from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone  



class User( models.Model) : 
    nom = models.CharField(max_length = 100)
    prenom = models.CharField(max_length = 100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length = 10)
    password = models.CharField(max_length = 5000)
    created_at = models.DateTimeField(auto_now_add = True)
    image = models.ImageField(upload_to='categories/')

    def __str__(self) : 
        return self.email
    def update_password(self, new_password):
        hashed_password = make_password(new_password)
        User.objects.filter(pk=self.pk).update(password=hashed_password)
    @staticmethod
    def get_user_by_email(email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        
        
class Token(models.Model) : 
    token = models.CharField(max_length = 5000)
    user = models.ForeignKey(User, on_delete= models.CASCADE,related_name="tokens_set")
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self) : 
        return self.user.email
    
    
class PasswordResetToken(models.Model) : 
    token = models.CharField(max_length = 5000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    validity = models.DateTimeField(default=timezone.now) 
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self) : 
        return self.user.email
import uuid

class Poste (models.Model) : 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    TYPE_CHOICES = (
        (0, 'offre'),
        (1, 'demande'),
    )
    type = models.IntegerField(choices = TYPE_CHOICES)
    image = models.ImageField(upload_to='categories/')
    date = models.DateTimeField( auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Evenement(Poste):
    intitule = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    lieu = models.CharField(max_length=100)
    contactinfo = models.CharField(max_length=200)
    
    
class EvenementClub(Evenement):
    club = models.CharField(max_length=50)
    
class EvenementSociale(Evenement):
    prix = models.DecimalField(max_digits=5 , decimal_places=5)


class Stage(Poste):
    TYPE_CHOICES = (
        (1, 'ouvrier'),
        (2, 'technicien'),
        (3, 'PFE'),
    )
    typeStg = models.IntegerField(choices =TYPE_CHOICES )
    societe = models.CharField(max_length=100)
    duree = models.IntegerField()
    sujet = models.CharField(max_length=500)
    contactinfo = models.CharField(max_length=200)
    spécialité = models.CharField(max_length=50)
    

class Logement(Poste):
    localisation = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    contactinfo = models.CharField(max_length=200)
  

class Transport(Poste):
    depart = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    heure_dep = models.DateTimeField()
    nbre_siéges = models.IntegerField()
    contactinfo = models.CharField(max_length=200)


class Recommendation(Poste):
    text = models.CharField(max_length=200)
    
   


    
    
class Reaction(models.Model):
    LIKE_CHOICES = (
        (True, 'Like'),
        (False, 'Dislike'),
    )
    post = models.ForeignKey(Poste, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.BooleanField(choices=LIKE_CHOICES,default=False)

    def __str__(self):
        return f"{self.user.email} reacted {self.get_reaction_type_display()} to {self.post.id}"
    
class Commentaire(models.Model):
    post = models.ForeignKey(Poste, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contenu = models.CharField(max_length=500, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
