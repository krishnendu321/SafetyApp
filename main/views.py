from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import UserRegisterForm
from .models import EmergencyContact, PoliceStation, SOSRequest

# Home View
def home(request):
    contacts = EmergencyContact.objects.all()
    stations = PoliceStation.objects.all()
    context = {
        'contacts': contacts,
        'stations': stations,
        'user': request.user
    }
    return render(request, 'main/home.html', context)

# Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})

# SOS View
@login_required
def sos(request):
    if not request.user.is_verified:
        return JsonResponse({
            'status': 'error',
            'message': 'Account not verified by admin'
        }, status=403)

    if request.method == 'POST':
        try:
            lat = request.POST.get('lat')
            lng = request.POST.get('lng')
            
            sos_request = SOSRequest.objects.create(
                user=request.user,
                latitude=lat,
                longitude=lng
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Emergency alert recorded!',
                'data': {
                    'id': sos_request.id,
                    'timestamp': sos_request.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    'location': f"{lat},{lng}"
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=400)