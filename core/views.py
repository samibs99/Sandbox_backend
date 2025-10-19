from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from core.models import User
import json

# ----------------------
# Login HTTP
# ----------------------
@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)
    
    data = json.loads(request.body)
    email = data.get("email")
    password = data.get("password")
    
    user = authenticate(request, email=email, password=password)
    
    if user is not None:
        login(request, user)
        return JsonResponse({"message": "Login successful", "role": user.role})
    else:
        return JsonResponse({"error": "Invalid credentials"}, status=401)

# ----------------------
# Créer un utilisateur (admin seulement)
# ----------------------
@csrf_exempt
@login_required
def create_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)
    
    if request.user.role != "ADMIN":
        return JsonResponse({"error": "Only admin can create users"}, status=403)
    
    data = json.loads(request.body)
    email = data.get("email")
    password = data.get("password")
    inst_name = data.get("inst_name")
    phone = data.get("phone")
    cnr = data.get("cnr")
    role = data.get("role")  # STUDENT ou TEACHER

    if not all([email, password, inst_name, phone, cnr, role]):
        return JsonResponse({"error": "Missing fields"}, status=400)
    
    user = User.objects.create_user(
        email=email,
        password=password,
        inst_name=inst_name,
        phone=phone,
        cnr=cnr,
        role=role
    )
    
    return JsonResponse({"message": f"User {user.email} created", "role": user.role})
