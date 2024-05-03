from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.hashers import make_password
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import  ListView, UpdateView, DeleteView, CreateView
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse, reverse_lazy
from .forms import DocumentForm, UserForm
from .models import User, Document
from django.contrib import messages

# Create your views here.



from django.shortcuts import render



# Shared Views
def login_form(request):
	return render(request, 'connexion/login.html')




from django.contrib import messages

def connect(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if 'first_login' not in request.session:
                # Stockez un indicateur dans la session de l'utilisateur pour marquer la première connexion
                request.session['first_login'] = True
            if user.is_admin or user.is_superuser:
                return redirect('admin') 
            else:
                return redirect('home')
        else:
            # Afficher un message d'erreur si le nom d'utilisateur ou le mot de passe est incorrect
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        # Vérifiez si l'utilisateur est déjà connecté
        if request.user.is_authenticated:
            # Redirigez l'utilisateur vers la page d'accueil ou une autre page pertinente
            return redirect('home')
    # Afficher la page de connexion en cas de méthode GET ou si l'authentification a échoué
    return render(request, 'connexion/login.html')


def deconnect(request):
    logout(request)
    # Rediriger l'utilisateur vers la page d'accueil après la déconnexion
    return redirect('home')

def registerView(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        # Vérifier si un utilisateur avec le même nom d'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe déjà.")
            return redirect('register')
        
        # Vérifier si un utilisateur avec la même adresse e-mail existe déjà
        if User.objects.filter(email=email).exists():
            messages.error(request, "Cette adresse e-mail est déjà utilisée.")
            return redirect('register')

        # Créer un nouvel utilisateur en utilisant le gestionnaire personnalisé
        user = User.objects.create_user(username=username, email=email, password=password)

        messages.success(request, 'Compte créé avec succès.')
        return redirect('login')
    else:
        return render(request, 'connexion/signup.html')
def register_form(request):
	return render(request, 'connexion/signup.html')



from django.urls import reverse


    
        

    # Renvoyez ces valeurs dans le contexte de votre template



"""
def reset_password(request):
    if request.method == 'POST':
        # Récupérer l'e-mail soumis par l'utilisateur dans le formulaire
        email = request.POST.get('email')

        # Vérifier si l'e-mail correspond à un utilisateur enregistré
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Si aucun utilisateur correspondant n'est trouvé, afficher un message d'erreur
            return render(request, 'reset_password.html', {'error_message': 'Aucun utilisateur trouvé avec cet e-mail.'})

        # Générer un lien de réinitialisation de mot de passe
        reset_password_link = "https://w01.com/reset-password/"

        # Rendre le contenu HTML du template d'e-mail avec les données personnalisées
        html_content = render_to_string('emails/password_reset.html', {'reset_password_link': reset_password_link})

        # Envoyer l'e-mail à l'utilisateur
        send_mail(
            'Réinitialisation de votre mot de passe',
            html_content,
            'votre_email@example.com',
            [email],
            html_message=html_content,
        )

        # Rediriger vers une page de confirmation
        return redirect('password_reset_confirmation')

    # Si la méthode de requête est GET, afficher le formulaire de réinitialisation de mot de passe
    return render(request, 'reset_password.html')
"""


@login_required
def client(request):
	return render(request, 'dashboard/finances.html')






def view_profile(request):
    user_profile = None
    if request.user.is_authenticated:
        user_profile = request.user
    else:
        user_profile = {
            'name': 'Your Name',
            'function': 'Function',
            'email': 'your@mail.com',
            'phone_number': 'Your Phone Number',
            'city': 'Your City',
            'website': 'Your Website',
            
        }
    return render(request, 'dashboard/index.html', {'user_profile': user_profile})


def view_profile_changed(request, slug):
    # Récupérer le profil de l'utilisateur correspondant au nom d'utilisateur passé dans l'URL
     user_profile = get_object_or_404(User, slug=slug)

    # Passer le profil récupéré à votre modèle de rendu
     return render(request, 'dashboard/index.html', {'user_profile': user_profile})


@login_required
def edit_profile(request):
    user_profile = request.user
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
        return redirect('profile_changed', slug=user_profile.slug)
    else:
        # Utilisez la méthode initial du formulaire pour définir les valeurs par défaut
        initial_data = {
            'name': user_profile.name if user_profile.name else 'Your Name',
            'function': user_profile.function if user_profile.function else 'Function',
            'email': user_profile.email if user_profile.email else 'Email',
            'email_bureau': user_profile.email_bureau if user_profile.email_bureau else 'Office Email',
            'city': user_profile.city if user_profile.city else 'Address',
            'phone_number': user_profile.phone_number if user_profile.phone_number else 'Phone Number',
            'office_number': user_profile.office_number if user_profile.office_number else 'Office Number',
            'website': user_profile.website if user_profile.website else 'Website',
            # Ajoutez d'autres champs ici avec leurs valeurs par défaut
        }
        form = UserForm(instance=user_profile, initial=initial_data)
    return render(request, 'dashboard/edit_profil.html', {'form': form})






def login_or_edit_profile(request):
    if request.user.is_authenticated:
        if 'first_login' in request.session:
            # Si l'utilisateur s'est déjà connecté avec succès mais n'est pas un nouvel utilisateur,
            # redirigez-le vers la page où il doit saisir son mot de passe pour accéder aux fonctionnalités supplémentaires.
            return redirect(reverse('testify'))
        else:
            # Si c'est la première connexion réussie, redirigez-le directement vers la page de modification de profil.
            return redirect(reverse('edit_profile'))
    else:
        # Si l'utilisateur n'est pas connecté du tout, redirigez-le vers la page de connexion.
        return redirect('connect')


def login_or_functions(request):
    if request.user.is_authenticated:
        if 'first_login' in request.session:
            # Si l'utilisateur s'est déjà connecté avec succès mais n'est pas un nouvel utilisateur,
            # redirigez-le vers la page où il doit saisir son mot de passe pour accéder aux fonctionnalités supplémentaires.
            return redirect(reverse('testify'))
        else:
            # Si c'est la première connexion réussie, redirigez-le directement vers la page de modification de profil.
            return redirect(reverse('fonctionalite'))
    else:
        # Si l'utilisateur n'est pas connecté du tout, redirigez-le vers la page de connexion.
        return redirect('connect')


def check_password_for_fonctionnalite(request):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        user = request.user
        if user.check_password(entered_password):
            return redirect('edit_profile')  # Redirige vers les fonctionnalités supplémentaires si le mot de passe est correct
        else:
            # Afficher un message d'erreur si le mot de passe est incorrect
            return render(request, 'dashboard/incorrect_pass.html')
    else:
        # Afficher le formulaire de saisie du mot de passe
        return render(request, 'dashboard/checkpass.html')
    
def check_password_for_menu(request):
    if request.method == 'POST':
        entered_password = request.POST.get('password')
        user = request.user
        if user.check_password(entered_password):
            return redirect('menu')  # Redirige vers les fonctionnalités supplémentaires si le mot de passe est correct
        else:
            # Afficher un message d'erreur si le mot de passe est incorrect
            return render(request, 'dashboard/incorrect_pass.html')
    else:
        # Afficher le formulaire de saisie du mot de passe
        return render(request, 'dashboard/check_menu.html')



def check_pass(request):
    return render(request,'dashboard/checkpass.html' )


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # To keep the user logged in
            return redirect('pass_changer')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'dashboard/change_password.html', {'form': form})

def password_change_done(request):
    return render(request, 'dashboard/change_password_done.html')




@login_required
def aabook_form(request):
	return render(request, 'dashboard/add_pdf.html')



@login_required
def aabook(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        pdf = request.FILES.get('pdf')
        current_user = request.user

        # Création d'un document lié à l'utilisateur actuel
        document = Document(title=title, pdf=pdf, user=current_user)
        document.save()
        
        messages.success(request, 'Ajout réussi')
        return redirect('albook')  # Rediriger vers la liste des documents après ajout
    else:
        messages.error(request, 'Erreur lors de l\'ajout du document')
        return redirect('aabook_form')  # Rediriger vers le formulaire d'ajout de document en cas d'erreur

 
 

class ABookListView(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'dashboard/list_pdf.html'
    context_object_name = 'docs'
    paginate_by = 3

    def get_queryset(self):
        # Filtrer les documents en fonction de l'utilisateur connecté
        return Document.objects.filter(user_id=self.request.user.id).order_by('-id')
    
"""   
class AManageUserprofil(LoginRequiredMixin, ListView):
    model= UserProfile
    template_name = 'dashboard/manage_profil.html'
    context_object_name = 'Uses'
    paginate_by= 3
    
    def get_queryset(self) -> QuerySet[Any]:
         return UserProfile.objects.order_by('name')
""" 


def PageBuilding(request):
    return render(request, 'dashboard/page_not_done.html')


class AeditView(LoginRequiredMixin, UpdateView):
    model= User
    form_class = UserForm
    template_name= 'dashboard/edit_profil.html'
    success_url= reverse_lazy('home')
    success_message = 'Sauvegarder avec succés'
    

@login_required
def Menu(request):
	return render(request, 'dashboard/menu.html')


def login_or_menu(request):
    if request.user.is_authenticated:
        return redirect(reverse('menu'))
    else:
        return redirect('connect')

@login_required
def Transport(request):
	return render(request, 'dashboard/transport.html')


@login_required
def Finance(request):
	return render(request, 'dashboard/finances.html')



class AManageBook(LoginRequiredMixin,ListView):
	model = Document
	template_name = 'dashboard/manage.html'
	context_object_name = 'docs'
	paginate_by = 3

	def get_queryset(self):
            return Document.objects.filter(user=self.request.user).order_by('-id')


class AeditDocView(LoginRequiredMixin, UpdateView):
    model= Document
    form_class = DocumentForm
    template_name= 'dashboard/edit_doc.html'
    success_url= reverse_lazy('ambook')
    success_message = 'Sauvegarder avec succés'
    


class ADeleteBook(LoginRequiredMixin,DeleteView):
	model = Document
	template_name = 'dashboard/delete.html'
	success_url = reverse_lazy('ambook')
	success_message = 'Data was dele successfully'
 
 
 
 
 #admin
def dashboard(request):
	user = User.objects.all().count()

	context = { 'user':user}

	return render(request, 'admin/home.html', context)
    
def create_user_form(request):
    choice = ['1', '0', 'Admin', 'client']
    choice = {'choice': choice}

    return render(request, 'admin/add_user.html', choice)


class ListUserView(generic.ListView):
    model = User
    template_name = 'admin/list_user.html'
    context_object_name = 'users'
    paginate_by = 4
 
class CreateUserView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'admin/add_user.html'
    success_message = 'Compte utilisateur créé avec succès'

    def get_success_url(self):
    # Récupérer l'utilisateur créé
     created_user = self.object
    # Rediriger vers la page de profil de l'utilisateur créé en utilisant son nom
     return reverse_lazy('profile_detail', kwargs={'name': created_user.name})

""" 
def create_user_form(request):
    choice = ['1', '0', 'Admin', 'client']
    choice = {'choice': choice}

    return render(request, 'admin/add_user.html', choice)

from django.contrib.auth.models import User

from .models import User  # Importez votre modèle User

def create_user(request):
    choice = ['1', '0', 'Admin', 'client']
    choice = {'choice': choice}
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        email_bureau = request.POST['email_bureau']
        number = request.POST['numero']
        office_number = request.POST['numero_bureau']
        adress = request.POST['city']
        site = request.POST['website']
        photo = request.FILES['image']
        password = request.POST['password']
        password = make_password(password)
        userType=request.POST['userType']
        
        # Utilisez le gestionnaire personnalisé CustomUserManager pour créer un utilisateur
        #user_manager = User.objects
        if userType == "client":
            user = User.objects.create_user(name=name,  email=email, email_bureau= email_bureau, phone_number =number, office_number= office_number, photo=photo, password=password, city= adress, website= site,is_client=True)

            messages.success(request, 'Member was created successfully!')
            return redirect('wluser')
        elif userType == "Admin":
            user = User.objects.create_user(name=name, email=email, email_bureau= email_bureau, phone_number =number, office_number= office_number, photo= photo, password=password,city= adress, website= site,is_admin=True)
            
            messages.success(request, 'Member was created successfully!')
            return redirect('wluser')   
        else:
            messages.success(request, 'Member was not created')
            return redirect('create_user_form')
    else:
        return redirect('create_user_form')
"""  