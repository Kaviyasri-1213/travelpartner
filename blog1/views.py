from django.shortcuts import render,redirect
from .models import Signup
from django.contrib import messages
from django.contrib.auth.hashers import check_password,make_password



# Create your views here.
def home(request):
    return render(request,'index.html')
def login(request):
     if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            messages.error(request,"Please fill all the fields")
            return redirect('login')

        try:
            user_obj = Signup.objects.get(username=username)
            if check_password(password, user_obj.password):
                request.session['username'] = user_obj.username 
                request.session['password'] = user_obj.password  
                messages.success(request, "Login successful!")
                return redirect('desti')  
            else:
                messages.error(request, "Invalid password. Please try again.")
        except Signup.DoesNotExist:
            messages.error(request, "User does not exist. Please sign up first.")
     return render(request,'login.html')
 
def signup(request):
     if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('password')
        repeatpass = request.POST.get('repeatpass')
        email = request.POST.get('emailid')

        if password != repeatpass:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')
        if Signup.objects.filter(email=email).exists():
            messages.error(request, "Email already registered, please login")
            return redirect('signup')

        if Signup.objects.filter(username=user).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

        obj = Signup()
        obj.username = user
        obj.password =  make_password(password)
        obj.email = email
        obj.save()

        messages.success(request, "Signup successful! Please login.")
        return redirect('login')
     return render(request, 'signup.html')

def desti(request):
    destination_prefill = request.GET.get('destination') or request.session.get('searched_destination', '') 

    if request.method == 'POST':
        destination = request.POST.get('destination', '').strip()
        experience = request.POST.get('experience', '').strip()
        duration = request.POST.get('duration', '').strip()
        budget = request.POST.get('budget', '').strip()
        start_date = request.POST.get('start_date', '')
        email = request.POST.get('email', '').strip()


        if not destination and not experience:
            messages.error(request, "Please enter a destination or choose a travel type.")
            ctx = {'destination': destination,'experience': experience,'duration': duration,'budget': budget,'start_date': start_date}
            return render(request, 'desti.html', ctx)

        budget_val = int(budget) if budget else 0
        duration_val = int(duration) if duration else 0

        recommendations = []

        # Logic based suggestions
        if experience == 'beach' or budget_val < 20000:
            recommendations.append({'name': 'Goa','reason': 'Beach fun + budget friendly.','img': 'goa.jpg'})
            recommendations.append({'name': 'Pondicherry','reason': 'Clean beaches & French vibes.','img': 'pondi.jpg'})
            recommendations.append({'name': 'Andaman','reason': 'Crystal-clear water & scuba diving.','img': 'andaman.jpg'})
            recommendations.append({'name':'Bali','reason':'Beautiful beaches, temples & perfect for couples/friends.','img':'bali.jpg'})
        if experience == 'adventure' or duration_val >= 5:
            recommendations.append({'name': 'Manali','reason': 'Best for trekking & adventure.','img': 'manali.jpg'})
            recommendations.append({'name': 'Rishikesh','reason': 'River rafting & adventure sports hub.','img': 'risk.jpg'})
            recommendations.append({'name': 'Ladakh','reason': 'Bike rides & mountain adventure.','img': 'ladakh.jpg'})

        if experience == 'city' or budget_val > 50000:
            recommendations.append({'name': 'Dubai','reason': 'Luxury travel & skyscrapers.','img': 'dubai.jpg'})
            recommendations.append({'name': 'Singapore','reason': 'Clean, modern city with attractions.','img': 'singam.jpg'})
            recommendations.append({'name': 'Malaysia','reason': 'City + nature mixed experience.','img': 'malaysia.jpg'})

        if experience == 'culture':
            recommendations.append({'name': 'Kerala','reason': 'Backwaters & calm relaxation.','img': 'kerala.jpg'})
            recommendations.append({'name': 'Varanasi','reason': 'Indian culture + spiritual vibes.','img': 'varanashi.jpg'})
            recommendations.append({'name': 'Hampi','reason': 'Ancient temples & peaceful scenery.','img': 'hampi.jpg'})
            recommendations.append({'name': 'Thailand','reason': 'Affordable international trip with temples, nightlife & beaches.','img': 'thai.jpg'})

        # remove duplicates
        seen = set()
        unique_recs = []
        for r in recommendations:
            if r['name'].lower() not in seen:
                seen.add(r['name'].lower())
                unique_recs.append(r)

        return render(request, 'recommen.html', {
            'results': unique_recs,
            'start_date': start_date,
            'budget': budget,
            'email': email})

    return render(request, 'desti.html')
def recommen(request):
    return redirect('desti')

def viewpack(request):
    # This receives data passed from recommen()
    date = request.GET.get('date')
    place = request.GET.get('place')
    budget = request.GET.get('budget')
    email = request.GET.get('email')


    return render(request, "view.html", {
        'date': date,
        'place': place,
        'budget': budget,
        'email': email

    })

def confirmbook(request):
        email = request.GET.get('email')
        return render(request,'confirm.html' ,{
        'email': email
    })


def help(request):
    return render(request,'help.html')
def contact(request):
    return render(request,'contact.html')
def about(request):
    return render(request,'about.html')
def terms(request):
    return render(request,'terms.html')
def poli(request):
    return render(request,'poli.html')