import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from flask import redirect
from myapp.models import User
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse



#### render functions #######

from django.shortcuts import render

from myapp.utils import token_response
from myapp.models import *

def create_account_view(request):
    return render(request, 'myapp/create_account.html')
@csrf_exempt
def login_view(request):
    return render(request, 'myapp/login.html')

def dashbord_view(request, token):
    token = Token.objects.filter(token = token).first()
    if token : 
        return render(request, 'myapp/posts.html')
    

def creation_posts(request) : 
    return render(request,'myapp/recommendation.html')

def creation_transport(request) : 
    return render(request,'myapp/transport.html')

def creation_logement(request) : 
    return render(request,'myapp/logement.html')

def creation_stage(request) : 
    return render(request,'myapp/stage.html')
def my_posts_view(request,token) : 
    return render(request,'myapp/mes_postes.html')
def profile_veiw(request,token) : 
    return render(request,'myapp/user_details.html')


def notification_detail(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    
    # Marquer la notification comme lue si elle appartient à l'utilisateur et n'est pas encore lue
    if notification.user == request.user and not notification.read:
        notification.read = True
        notification.save()
    
    # Passer la notification et son message à la vue pour l'affichage
    message = notification.message  # Supposons que le champ message contient le contenu du message
    context = {
        'notification': notification,
        'message': message,
    }
    return render(request, 'student_help/notification_detail.html', context)
    
@csrf_exempt
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def create_account(request):
    if request.method == 'POST':
        try:
            data = request.data

            nom = data.get('nom')
            prenom = data.get('prenom')

            email = data.get('email')
            phone = data.get('phone')
            password = data.get('password')


            if email and phone and password:
                print(f"Trying to find Otp for phone: {phone}")
               
                User.objects.create(nom=nom, prenom=prenom, email=email, phone=phone, password=password)
                # otp_obj.delete()
                return HttpResponse("account created successfully")
            else:
                error_message = "Invalid data provided. "
                if not email:
                    error_message += "Email is required. "
                if not phone:
                    error_message += "Phone is required. "
                if not password:
                    error_message += "Password is required. "
                if not nom:
                    error_message += "nom is required. "
                if not prenom:
                    error_message += "prenom is required. "
                print(f"Error message: {error_message.strip()}")

                return HttpResponse(error_message.strip(), status=400)

        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON format in the request body", status=400)

        except Exception as e:
            print(f"Error: {str(e)}")
            return HttpResponse("An error occurred while processing the request", status=500)

    return HttpResponse("Invalid request method", status=405)



from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import json
from rest_framework.permissions import AllowAny


@csrf_exempt 
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([AllowAny]) 
def login_user(request):
    if request.method =='POST'  :
        email = request.data.get('email')
        password = request.data.get('password')
        if email:
            user = User.objects.filter(email=email).first()
        
            password1 = user.password if user else None
        else:
            return JsonResponse({'error': 'data missing'}, status=400)

        if user :
            if password == password1:
                return token_response(user)
                
            else :
                return JsonResponse({'response':'mdpincorrecte'},status = 400)
        else:
            return JsonResponse({'error': 'incorrect password'}, status=400)
    
    


@csrf_exempt 
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def create_post(request,  type_post , token):
    token_obj = Token.objects.filter(token = token).first()
    user_obj = token_obj.user
    if request.method == "POST" and token_obj:
            if type_post == 'evenementclub':
                type = request.data.get("type")
                image_file = request.FILES.get("image") 
                intitule = request.data.get("intitule")
                description = request.data.get("description")
                lieu = request.data.get("lieu")
                contactinfo = request.data.get("contactinfo")
                club = request.data.get("club")
                stage = EvenementClub.objects.create(
                    type=type,
                    image=image_file,
                    intitule = intitule,
                    description = description,
                    lieu = lieu,
                    contactinfo=contactinfo,
                    club = club,
                    user = user_obj
                    
                )
                stage.save()
                reaction = Reaction.objects.create(
                    post = stage,
                    user = user_obj,
                    
                )
                reaction.save()
            elif type_post == 'evenementsociale':
                type = request.data.get("type")
                image_file = request.FILES.get("image") 
                intitule = request.data.get("intitule")
                description = request.data.get("description")
                lieu = request.data.get("lieu")
                contactinfo = request.data.get("contactinfo")
                prix = request.data.get("prix")
                
                stage = EvenementSociale.objects.create(
                    type=type,
                    image=image_file,
                    intitule = intitule,
                    description = description,
                    lieu = lieu,
                    contactinfo=contactinfo,
                    prix = prix,
                    user = user_obj
                    
                )
                stage.save()
                reaction = Reaction.objects.create(
                    post = stage,
                    user = user_obj,
                    
                )
                reaction.save()
            elif type_post == 'stage':
                type = request.data.get("type")
                image_file = request.FILES.get("image") 
                societe = request.data.get("societe")
                duree = request.data.get("duree")
                sujet = request.data.get("sujet")
                contactinfo = request.data.get("contactinfo")
                spécialité = request.data.get("spécialité")
                typeStg = request.data.get("typeStg")
                stage = Stage.objects.create(
                    type=type,
                    image=image_file,
                    societe=societe,
                    duree=duree,
                    sujet=sujet,
                    contactinfo=contactinfo,
                    spécialité=spécialité,
                    typeStg=typeStg,
                    user = user_obj
                )
                stage.save()
                reaction = Reaction.objects.create(
                    post = stage,
                    user = user_obj,
                    
                )
                reaction.save()
                
            elif type_post == 'logement':
                type = request.data.get("type")
                image_file = request.FILES.get("image") 
                localisation = request.data.get("localisation")
                contactinfo = request.data.get("contactinfo")
                description = request.data.get("description")
                stage = Logement.objects.create(
                    type=type,
                    image=image_file,
                    contactinfo=contactinfo,
                    description=description,
                    localisation=localisation,
                    user = user_obj
                )
                stage.save()
                reaction = Reaction.objects.create(
                    post = stage,
                    user = user_obj,
                    
                )
                reaction.save()
            elif type_post == 'transport':
                type = request.data.get("type")
                image_file = request.FILES.get("image") 
                depart = request.data.get("depart")
                destination = request.data.get("destination")
                heure_dep = request.data.get("heure_dep")
                nbre_siéges = request.data.get("nbre_siéges")
                contactinfo = request.data.get("contactinfo")
                stage = Transport.objects.create(
                    type=type,
                    image=image_file,
                    depart=depart,
                    destination=destination,
                    heure_dep = heure_dep,
                    nbre_siéges = nbre_siéges,
                    contactinfo=contactinfo,
                    user = user_obj
                )
                stage.save()
                reaction = Reaction.objects.create(
                    post = stage,
                    user = user_obj,
                    
                )
                reaction.save()
            elif type_post == 'recommendation':
                type = request.data.get("type")
                image_file = request.FILES.get("image") 
                text = request.data.get("text")
                stage = Recommendation.objects.create(
                    type=type,
                    image=image_file,
                    text=text,
                    user = user_obj
                   
                )
                stage.save()
                reaction = Reaction.objects.create(
                    post = stage,
                    user = user_obj,
                    
                )
                reaction.save()
            else:
                return JsonResponse({'error': 'Type de poste non valide'})
            
            return JsonResponse({'success': f'Poste de type {type_post} créé avec succès'})
        
from django.shortcuts import render

from django.shortcuts import render

def get_specific_post_data(post):
  if isinstance(post, Evenement):
    return {
        'intitule': post.intitule,
        'description': post.description,
        'lieu': post.lieu,
        'contactinfo': post.contactinfo,
    }
  elif isinstance(post, EvenementClub):
    return {
        'club': post.club,
        **get_specific_post_data(post)  
    }
  elif isinstance(post, EvenementSociale):
    return {
        'prix': post.prix,
        **get_specific_post_data(post)  
    }
  elif isinstance(post, Stage):
    return {
        'typeStg': post.get_typeStg_display(),  
        'societe': post.societe,
        'duree': post.duree,
        'sujet': post.sujet,
        'spécialité': post.spécialité,
    }
  elif isinstance(post, Logement):
    return {
        'localisation': post.localisation,
        'description': post.description,
    }
  elif isinstance(post, Transport):
    return {
        'depart': post.depart,
        'destination': post.destination,
        'heure_dep': post.heure_dep,
        'nbre_siéges': post.nbre_siéges,
    }
  elif isinstance(post, Recommendation):
    return {
        'text': post.text,
    }
  else:
    return {}  

def all_posts(request, token):
    token_obj = Token.objects.filter(token=token).first()
    token = token
    print("heeyeeeeeeeeeeeeeee",token)
    post_data = {
        'offres': [],  
        'demandes': [],  
    }

    all_postes = Poste.objects.all()
    for post in all_postes:
        reactions_count = Reaction.objects.filter(post__id=post.id,reaction_type = True).count()  # Nombre de réactions
        reaction = Reaction.objects.filter(post__id=post.id,).first()
        commentaires = Commentaire.objects.filter(post__id=post.id)
        commentaires_data = []
        for commentaire in commentaires:
            commentaires_data.append({
                'user': commentaire.user,
                'contenu': commentaire.contenu,
            })
        if post.type == Poste.TYPE_CHOICES[0][0]:  
            post_data['offres'].append({
                'id': post.id,
                'image': post.image.url if post.image else None,
                'date': post.date,
                'userimage': post.user.image,
                'username': post.user.nom,
                'prenom': post.user.prenom,
                'reaction': reaction.reaction_type,
                'commentaires': commentaires_data,
                'token' : token,
                'reactions_count': reactions_count, 

                **get_specific_post_data(post),
            })
        elif post.type == Poste.TYPE_CHOICES[1][0]:  
            post_data['demandes'].append({
                'id': post.id,
                'image': post.image.url if post.image else None,
                'date': post.date,
                'userimage': post.user.image,
                'username': post.user.nom,
                'prenom': post.user.prenom,
                'reaction': reaction.reaction_type,
                'commentaires': commentaires_data,
                'token' : token,
                'reactions_count': reactions_count, 

                **get_specific_post_data(post),
            })
    context = {'post_data': post_data}
    return render(request, 'myapp/posts.html', context)

from django.contrib.auth.decorators import login_required
def my_posts(request, token):
    token_obj = Token.objects.filter(token=token).first()
    user_obj = token_obj.user
    post_data = {
        'offres': [],  
        'demandes': [],  
    }

    all_postes = Poste.objects.filter(user = user_obj)
    for post in all_postes:
        reaction = Reaction.objects.filter(post__id=post.id).first()
        commentaires = Commentaire.objects.filter(post__id=post.id)
        commentaires_data = []
        for commentaire in commentaires:
            commentaires_data.append({
                'user': commentaire.user,
                'contenu': commentaire.contenu,
            })
        if post.type == Poste.TYPE_CHOICES[0][0]:  
            post_data['offres'].append({
                'id': post.id,
                'image': post.image.url if post.image else None,
                'date': post.date,
                'userimage': post.user.image,
                'username': post.user.nom,
                'prenom': post.user.prenom,
                'reaction': reaction.reaction_type,
                'commentaires': commentaires_data,
                'token' : token_obj.token,
                **get_specific_post_data(post),
            })
        elif post.type == Poste.TYPE_CHOICES[1][0]:  
            post_data['demandes'].append({
                'id': post.id,
                'image': post.image.url if post.image else None,
                'date': post.date,
                'userimage': post.user.image,
                'username': post.user.nom,
                'prenom': post.user.prenom,
                'reaction': reaction.reaction_type,
                'commentaires': commentaires_data,
                'token' : token_obj.token,
                **get_specific_post_data(post),
            })
    context = {'post_data': post_data}
    return render(request, 'myapp/mes_postes.html', context)



@csrf_exempt 
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def like_post(request, post_id,token):
    if request.method =="POST":
        # Récupérez le poste correspondant à l'ID fourni
        try:
            post = Poste.objects.get(pk=post_id)
        except Poste.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)
        try:
            token_obj = Token.objects.get(token=token)
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Token not found'}, status=404)
        
        user_obj = token_obj.user
        reaction, created = Reaction.objects.get_or_create(user=user_obj, post=post)
        
        # Inversez la réaction (like ou dislike) si elle existe déjà
        reaction.reaction_type = not reaction.reaction_type
        reaction.save()

        return JsonResponse({'success': reaction.reaction_type})
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
@csrf_exempt
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def create_comment(request,post_id,token):
    if request.method == 'POST':
        # Récupérer les données du commentaire depuis la requête POST
        try:
            post = Poste.objects.get(pk=post_id)
        except Poste.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)
        try:
            token_obj = Token.objects.filter(token=token).first()
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Token not found'}, status=404)
        
        user_obj = token_obj.user
        
        contenu = request.POST.get('contenu')
        
        # Vérifier si toutes les données requises sont présentes
        if  contenu:
            # Créer le commentaire dans la base de données
            commentaire = Commentaire.objects.create(
                post=post,
                user = user_obj,
                contenu=contenu
            )
            # Retourner une réponse JSON pour indiquer que le commentaire a été créé avec succès
            return JsonResponse({'success': True, 'comment_id': commentaire.id})
        else:
            # Retourner une réponse JSON avec un message d'erreur si des données requises sont manquantes
            return JsonResponse({'error': 'Missing required data'}, status=400)
    else:
        # Retourner une réponse JSON avec un message d'erreur si la méthode de requête n'est pas autorisée
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])  
def get_comments(request, post_id):
    if request.method == 'GET':
        # Récupérer tous les commentaires associés au poste donné
        comments = Commentaire.objects.filter(post__id=post_id)
        
        # Construire une liste de dictionnaires contenant les détails de chaque commentaire
        comments_list = []
        for comment in comments:
            comment_data = {
                'id': comment.id,
                'user': comment.user.email,
                'contenu': comment.contenu,
            }
            comments_list.append(comment_data)
        
        # Retourner une réponse JSON avec la liste des commentaires
        return JsonResponse({'comments': comments_list})
    else:
        # Retourner une réponse JSON avec un message d'erreur si la méthode de requête n'est pas autorisée
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    

@csrf_exempt
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication]) 
def create_comment(request,post_id,token) :
    token_obj = Token.objects.filter(token = token).first()
    post = Poste.objects.filter(id = post_id).first()
    user_obj = token_obj.user
    if request.method =="POST" : 
        comment = request.data.get("comment")
        if comment :
            comment_create = Commentaire.objects.create(post = post , user = user_obj, contenu = comment)
            comment_create.save
            return JsonResponse({"message":"bien"})
        else : 
            return JsonResponse({"erreur":"no"},status = 500)
    else : 
        return JsonResponse({"erreur":"no"},status = 400)
    
from django.http import JsonResponse
@csrf_exempt
@api_view(['DELETE'])
def delete_post(request, post_id, token):
    # Vérifiez le jeton pour l'authentification, la permission, etc.
    token_obj = Token.objects.filter(token=token).first()
    user_obj = token_obj.user
    
    # Récupérez le poste à supprimer
    post_to_delete = Poste.objects.get(id=post_id)
    
    # Assurez-vous que l'utilisateur actuel est l'auteur du poste
    if post_to_delete.user == user_obj:
        post_to_delete.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
    
    


from django.http import JsonResponse

@csrf_exempt
def user_details(request, token):
    if request.method == 'GET':
        token_obj = Token.objects.filter(token=token).first()
        if token_obj:
            user_email = token_obj.user.email
            if user_email:
                user = User.get_user_by_email(user_email)
                if user:
                    user_data = {
                        'nom': user.nom,
                        'prenom': user.prenom,
                        'email': user.email,
                        'phone': user.phone,
                        'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'image_url': user.image.url if user.image else None,
                    }
                    return JsonResponse({'success': True, 'user': user_data})
                else:
                    return JsonResponse({'success': False, 'message': 'Utilisateur non trouvé'})
            else:
                return JsonResponse({'success': False, 'message': 'Email non fourni'})
        else:
            return JsonResponse({'success': False, 'message': 'Token invalide'})
    else:
        return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})
