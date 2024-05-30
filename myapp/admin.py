from django.contrib import admin
from .models import Commentaire, Poste, User, Token, PasswordResetToken, Evenement, EvenementClub, EvenementSociale, Stage, Logement, Transport, Recommendation, Reaction

admin.site.register(User)
admin.site.register(Token)
admin.site.register(PasswordResetToken)
admin.site.register(EvenementClub)
admin.site.register(EvenementSociale)
admin.site.register(Stage)
admin.site.register(Logement)
admin.site.register(Transport)
admin.site.register(Recommendation)
admin.site.register(Reaction)
admin.site.register(Commentaire)
admin.site.register(Poste)


