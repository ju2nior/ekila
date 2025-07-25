from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.http import HttpResponseForbidden, JsonResponse
from .models import *
from .forms import *
from rest_framework import viewsets
from .serializers import EvenementSerializer
from rest_framework.permissions import IsAuthenticated



# ----------lister les evenements--------------

def list_evenement(request):
    evenement = Evenement.objects.all()
    if request.method == 'GET':
        name = request.GET.get('recherche')
        if name is not None:
            evenement = Evenement.objects.all()
    return render(request, 'list_evenement.html', {'evenement':evenement})

# -------------------Ajouter un evenement--------------



def create_evenement(request):
    if request.method == 'POST':
        form = EvenementForm(request.POST, request.FILES) 
        if form.is_valid():
            evenement = form.save(commit=False)
            try:
                evenement.reserver_ticket() 
                messages.success(request, "Événement créé avec succès.")
                return JsonResponse({'success': True})
            except ValidationError as e:
                return JsonResponse({'success': False, 'errors': str(e)})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = EvenementForm()
        return render(request, 'add_evenement.html', {'form': form})

    
# -------------Modifier un evenement-----------------


def update_evenement(request, pk):
    evenement = get_object_or_404(Evenement, pk=pk)
    if request.method == 'POST':
        form =EvenementForm(request.POST, instance=evenement)

        if form.is_valid():
            form.save()
            messages.success(request, "Événement mis à jour avec succès.")
            return redirect('evenement_list')
        else:
            print(form.errors)
            return render(request, 'evenement.html', {
                'form': form,
                'evenement': evenement,
                'errors': form.errors
            })
    else:
        form =EvenementForm(instance=evenement)
    return render(request, 'list_evenement.html', {'form': form, 'evenement': evenement})

# ------------delete un evenement ------------------



def delete_evenement(request, pk):
    evenement = get_object_or_404(Evenement, pk=pk)
    if request.method == 'POST':
        evenement.delete()
        return redirect('evenement_list')
    return render(request, 'delete_evenement.html', {'evenement': evenement})

# -------------- list_des_actions --------------



def list_actions(request):
    actions = Action.objects.all()
    return render(request, 'list_actions.html', {
        'actions': actions
    })

# -------------- creer_des_actions ---------

def create_action(request):
    if request.method == 'POST':
        form = ActionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_actions') 
    else:
        form = ActionForm()

    return render(request, 'create_action.html', {'form': form})

# -------------- update une action -------------

def update_action(request, action_id):
    action = get_object_or_404(Action, id=action_id)
    form = ActionForm(request.POST or None, instance=action)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('list_actions') 

    return render(request, 'update_action.html', {'form': form, 'action': action})

# --------------  delete une action ------------

def delete_action(request, action_id):
    action = get_object_or_404(Action, id=action_id)

    if request.method == 'POST':
        action.delete()
        return redirect('list_actions')

    return render(request, 'delete_action.html', {'action': action})

# ---------- type list----------------

def list_type(request):
   TypeEven = TypeEvenement.objects.all()
   return render(request, 'list_type.html', {
        'TypeEven': TypeEven
    })

# -------------- creer_des_Type ---------

def create_Type(request):
    if request.method == 'POST':
        form = TypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_Type') 
    else:
        form = TypeForm()

    return render(request, 'create_type.html', {'form': form})

# -------------- update un type -------------

def update_type(request, type_id):
    type = get_object_or_404(TypeEvenement, id=type_id)
    form = TypeForm(request.POST or None, instance=type)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('list_type') 

    return render(request, 'update_type.html', {'form': form, 'type': type})

# ------------- delete type------------------------

def delete_type(request, type_id):
    type = get_object_or_404(TypeEvenement, id=type_id)

    if request.method == 'POST':
        type.delete()
        return redirect('list_type')

    return render(request, 'delete_type.html', {'type': type})


# ------------- API-------------


class EvenementViewSet(viewsets.ModelViewSet):
    queryset = Evenement.objects.all()
    serializer_class = EvenementSerializer
    permission_classes = [IsAuthenticated]
