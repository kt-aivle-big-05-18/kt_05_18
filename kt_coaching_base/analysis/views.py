from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

def analysis (request):
    print(request.session.get("persona_id"))
    return render(request, "analysis/analysis.html")
# Create your views here.

def test (request):
    print("test")
    return JsonResponse({"message" : request.session.get("persona_id")[0]["id"]})