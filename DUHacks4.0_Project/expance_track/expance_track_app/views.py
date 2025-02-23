from django.shortcuts import redirect, render, get_object_or_404
from .models import Expence, UserReg
from django.contrib import messages
from .forms import ExpenseForm
from django.contrib.auth.decorators import login_required
import logging
logger = logging.getLogger(__name__)

# Create your views here.
def loginPage(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = UserReg.objects.get(email=email)
            if user.check_password(password):  
                request.session['user_id'] = user.userId
                logger.info(f"User {user.name} logged in successfully.")
                return redirect('mainPage')
            else:
                logger.warning(f"Invalid password for {email}")
                messages.error(request, "Invalid password. Try again.")
        except UserReg.DoesNotExist:
            logger.warning(f"Login attempt for non-existing user: {email}")
            messages.error(request, "User does not exist. Please sign up.")

    return render(request, 'core/login.html')

def signUp(request):
    if request.method == 'POST':
        name = request.POST['name']  
        email = request.POST['email']
        password = request.POST['password']

        if UserReg.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signUp')

        UserReg.objects.create(name=name, email=email, password=password)
        # user.save()

        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')

    return render(request, 'core/signUp.html')

@login_required
def mainPage(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = UserReg.objects.get(userId=user_id)

    # Fetch all expenses for the user
    expence = Expence.objects.filter(userId=user)

    # Calculate total expense
    total_expence = sum(expence.cost for expence in expence)

    return render(request, 'core/mainPage.html', {
        'expence': expence,
        'total_expence': total_expence
    })



@login_required
def add_expence(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)

            # Fetch the corresponding UserReg instance
            user_reg = UserReg.objects.get(userId=request.session.get('user_id'))

            expense.userId = user_reg  # Assign the correct UserReg instance
            expense.save()

            return redirect('mainPage')  # Redirect after saving

    else:
        form = ExpenseForm()

    return render(request, 'core/add_expence.html', {'form': form})


@login_required
def edit_expence(request,expence_id):
    expence = get_object_or_404(Expence,id = expence_id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expence)
        if form.is_valid():
            form.save()
            return redirect("mainPage")
    else:
        form = ExpenseForm(instance=expence)
    return render(request,'core/edit_expence.html',{'form':form}) 

@login_required
def delete_expence(request,expence_id):
    expence = get_object_or_404(Expence,id = expence_id)
    if request.method == 'POST':
        expence.delete()
        return redirect('mainPage')
    return render(request,'core/delete_expance.html',{'expence':expence})