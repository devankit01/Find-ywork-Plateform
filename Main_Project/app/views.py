from django.shortcuts import render, HttpResponse, redirect
from app.models import UserProfile, WorkerProfile, Work , Bid
from django.contrib import auth
from django.contrib.auth.models import User

# Create your views here.


def home(request):
    option = False

    if request.session.has_key('username'):
        print(request.session['username'])
        username = request.session['username']
        user = User.objects.get(username=username)
        option = True
        try:
            option = True
            UserProfile.objects.get(username=user)
            print('User HomePage')
            user = True
            worker = False

            return render(request, 'app/home.html', {'option': option, 'user': user, 'worker': worker})

        except:
            try:
                option = True
                WorkerProfile.objects.get(username=user)
                print('Worker HomePage')
                worker = True
                user = False
                objects =  Work.objects.all()
                return render(request, 'app/home.html', {'option': option, 'worker': worker, 'user': user, 'works' : objects})
            except:
                pass
    user = False
    worker = False
    return render(request, 'app/home.html', {'option': option, 'worker': worker, 'user': user})


def signup(request):
    if request.method == "POST":
        if request.POST['pass1'] == request.POST['pass2']:
            try:
                print(request.POST['phone'])
                user = User.objects.filter(username=request.POST['phone'])
                if len(user) == 0:
                    print(len(user))
                    raise User.DoesNotExist
                return render(request, 'app/accounts/signup.html', {'msg': 'Phone Number already exist.'})
            except User.DoesNotExist:
                fnname = request.POST['firstname']
                lname = request.POST['lname']
                phone = request.POST['phone']
                pass1 = request.POST['pass1']
                pass2 = request.POST['pass2']
                account = request.POST['profile']
                pincode = request.POST['pin']
                print(request.POST['profile'])
                user = User.objects.create_user(
                    first_name=fnname, last_name=lname, password=pass1, email="", username=phone)

                if account == '0':
                    print('User')
                    data = {
                        'fname': fnname,
                        'lname': lname,
                        'phone': phone,
                        'pass1': pass1,
                        'pass2': pass2,
                        'account': account,
                        'pincode': pincode,
                    }
                    profile = UserProfile(
                        phone=data['phone'], pincode=data['pincode'], username=user, address="")
                    try:
                        user.save()
                        profile.save()
                    except:
                        return HttpResponse('<h1>Something Went Wrong</h1>')

                elif account == '1':
                    print('Worker')
                    occupation = request.POST['occupation']
                    experience = request.POST['exp']
                    rupees = request.POST['money']
                    hourorday = request.POST['hd']

                    data = {
                        'fname': fnname,
                        'lname': lname,
                        'phone': phone,
                        'pass1': pass1,
                        'pass2': pass2,
                        'account': account,
                        'pincode': pincode,
                        'occupation': occupation,
                        'experience': experience,
                        'rupees': rupees,
                        'hourorday': hourorday,
                    }
                    profile = WorkerProfile(phone=data['phone'], pincode=data['pincode'], occupation=data['occupation'],
                                            experience=data['experience'], rupees=data['rupees'], hourorday=data['hourorday'], username=user, address="")
                    print(profile)
                    try:
                        user.save()
                        profile.save()
                    except:
                        return HttpResponse('<h1>Something Went Wrong</h1>')
                print(data)
                return render(request, 'app/accounts/signup.html', {'msg': 'Account successfully Created'})
        return render(request, 'app/accounts/signup.html', {'msg': "Password do not matched ❌"})
    return render(request, 'app/accounts/signup.html')


def signin(request):
    if request.method == "POST":
        try:
            username = request.POST['phone']
            password = request.POST['pass']
            print(username, password)
            User.objects.get(username=username)
            user_authenticate = auth.authenticate(
                username=username, password=password)
            if user_authenticate is not None:
                auth.login(request, user_authenticate)
                request.session['username'] = username
                print('yes')
                data = User.objects.get(username=username)
                try:
                    UserProfile.objects.get(username=data)
                    print('User Home')
                    return redirect('profile')
                except:
                    try:
                        WorkerProfile.objects.get(username=data)
                        print('Worker Home')
                        return redirect('profile')
                    except:
                        pass
            else:
                return render(request, 'app/accounts/signin.html', {'msg': 'Invalid Credentials'})
        except:
            return render(request, 'app/accounts/signin.html', {'msg': 'Not a valid User'})

    return render(request, 'app/accounts/signin.html')


def profile(request):
    if request.session.has_key('username'):
        try:
            user = User.objects.get(username=request.session['username'])
            data = UserProfile.objects.get(username=user)
            return render(request, 'app/user/userprofile.html', {'option': True, 'data': data})
        except:
            try:
                user = User.objects.get(username=request.session['username'])
                data = WorkerProfile.objects.get(username=user)
                return render(request, 'app/worker/workerprofile.html', {'option': True, 'data': data, 'btn': True})
            except:
                return HttpResponse('Error 404')

    return HttpResponse('Error 404')


def editprofile(request):
    if request.method == 'POST':
        fname = request.POST['firstname']
        lname = request.POST['lname']
        phone = request.POST['phone']
        address = request.POST['address']
        pincode = request.POST['pin']
        try:
            user = User.objects.get(username=request.session['username'])
            data = UserProfile.objects.get(username=user)
            user.first_name = fname
            user.last_name = lname
            data.phone = phone
            data.pincode = pincode
            data.address = address
            user.save()
            data.save()
            return redirect('profile')
        except:
            try:
                gender = request.POST['gender']
                occupation = request.POST['occupation']
                experience = request.POST['exp']
                rupees = request.POST['money']
                hourorday = request.POST['hd']
                user = User.objects.get(username=request.session['username'])
                data = WorkerProfile.objects.get(username=user)
                user.first_name = fname
                user.last_name = lname
                data.phone = phone
                data.address = address
                data.pincode = pincode
                data.gender = gender
                data.occupation = occupation
                data.experience = experience
                data.rupees = rupees
                data.hourorday = hourorday
                data.save()
                user.save()
                print(data, user)
                return redirect('profile')
            except:
                pass

    else:
        if request.session.has_key('username'):
            try:
                user = User.objects.get(username=request.session['username'])
                data = UserProfile.objects.get(username=user)
                print(user.first_name)
                return render(request, 'app/user/useredit.html', {'option': True, 'data': data})
            except:
                try:
                    user = User.objects.get(
                        username=request.session['username'])
                    data = WorkerProfile.objects.get(username=user)
                    print(user.first_name)
                    return render(request, 'app/worker/workeredit.html', {'option': True, 'data': data})
                except:
                    return HttpResponse('Error 404')
        return HttpResponse('Error 404')


def logout(request):
    try:
        del request.session['username']
        print('Logout')
    except:
        pass
    return redirect('/')


def seeprofile(request, key):
    try:
        user = User.objects.get(username=key)

        if UserProfile.objects.filter(username=user).exists():
            print('User Exist')
            return HttpResponse(user)
        if WorkerProfile.objects.filter(username=user).exists():
            data = WorkerProfile.objects.get(username=user)
            session_user = User.objects.get(
                username=request.session['username'])
            if session_user == user:
                btn = True
            else:
                btn = False
            print('Worker Exist')
            return render(request, 'app/worker/workerprofile.html', {'data': data, 'user': user, 'btn': btn, 'option': True})

        return HttpResponse(user)

    except:
        return HttpResponse('Error 404')


# About page
def about(request):
    option = checksession(request)
    return render(request, 'app/aboutsite.html', {'option': option})


# def search(request):
#     option = checksession(request)
#     return render(request, 'app/worker/searchworker.html', {'option': option})


def myworks(request):
    option = checksession(request)
    user = User.objects.get(username=request.session['username'])
    data = UserProfile.objects.get(username=user)
    if request.method == 'POST':
        title = request.POST.get('work_name')
        amount = request.POST.get('amount')
        days = request.POST.get('days')
        category = request.POST.get('occupation')
        description = request.POST.get('description')
        print(title, amount, days ,category, description)

        newWork = Work.objects.create(title=title, maxamount=amount, maxdays=days, category=category, description=description, creator = data )
        newWork.save()
        return redirect('myworks')
        
    else:
        try:
            if option and data:
                print(user)
                works = Work.objects.filter(creator=data)
                print(works)
                return render(request, 'app/user/myworks.html', {'option': option, 'works': works})
        except:
            return HttpResponse('Error 404')



def checksession(request):
    if request.session.has_key('username'):
        option = True
    else:
        option = False
    return option


def search(request):
    if request.method == "GET":
        print('hi')
        search = request.GET.get('q')       # do some research what it does
        print(search)

        status1 = WorkerProfile.objects.filter(pincode=search)
        print(status1)

        status2 =WorkerProfile.objects.filter(occupation=search)
        print(list(status1) +  list(status2))

        # model.objects.filter(Q(first_name=foo) | Q(last_name=bar))

        return render(request, 'app/worker/searchworker.html')
    else:
        print('hi')


def workDescription(request, id):
    option = checksession(request)

    workObj = Work.objects.get(id=id)

    try:
        userObj = User.objects.get(username = request.session['username'])
        workerProfile = WorkerProfile.objects.get(username = userObj)
        print(workerProfile)
    except: 
        workerProfile = None

    # Bid Place
    response = Bid.objects.filter(worker = workerProfile, work=workObj)
    print(response)

    if len(response) == 0:
        print(response.count())
        bid = False
        bidData = None
    else:
        bidData = Bid.objects.get(worker = workerProfile, work=workObj)
        print(bidData)
        bid = True


    if request.method == 'POST':
        bidamount = request.POST.get('bidamount')
        biddays = request.POST.get('biddays')
        print(bidamount, biddays)

        newBid = Bid.objects.create(worker = workerProfile, work=workObj , proposal_price = bidamount , proposal_days = biddays)
        newBid.save()

        return redirect('workDescription')

    return render(request, 'app/user/workDescription.html',{'obj' : workObj , 'option' : option , 'bid' : bid ,'workerProfile' : workerProfile, 'bidData' : bidData})