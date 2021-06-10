from django.shortcuts import render, HttpResponse, redirect
from app.models import *
from django.contrib import auth
from django.contrib.auth.models import User
import random
from datetime import date

today = date.today()
# Create your views here.
from twilio.rest import Client
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)


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

            workerObj = WorkerProfile.objects.all()

            return render(request, 'app/home.html', {'option': option, 'user': user, 'worker': worker, 'workerObj': workerObj})

        except:
            try:
                option = True
                WorkerProfile.objects.get(username=user)
                print('Worker HomePage')
                worker = True
                user = False
                objects = Work.objects.all()
                return render(request, 'app/home.html', {'option': option, 'worker': worker, 'user': user, 'works': objects})
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
                return redirect('signin')
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
                    return redirect('home')
                except:
                    try:
                        WorkerProfile.objects.get(username=data)
                        print('Worker Home')
                        return redirect('home')
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
                obj = Bid.objects.filter(worker = data , isassigned = True)
                ratings = []
                for i in obj:
                    work = Work.objects.get(id = i.work.id)
                    get = Rating.objects.filter(work = work)
                    ratings.extend(get)
                print(ratings)
                return render(request, 'app/worker/workerprofile.html', {'option': True, 'data': data, 'btn': True , 'ratings': ratings})
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
    if True:
        try:
            user = User.objects.get(username=key)
            data = WorkerProfile.objects.get(username=user)
            print(user.first_name)

            # Get ratings ###############################
            obj = Bid.objects.filter(worker = data , isassigned = True)
            ratings = []
            for i in obj:
                work = Work.objects.get(id = i.work.id)
                get = Rating.objects.filter(work = work)
                ratings.extend(get)
            print(ratings)
            ###############################################
            return render(request, 'app/seeprofile.html', {'option': True, 'data': data,'ratings': ratings})
        except:
            return HttpResponse('Error 404')
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
        amount = request.POST.get('amount', None)
        days = request.POST.get('days', None)
        category = request.POST.get('occupation')
        description = request.POST.get('description')
        print(title, amount, days, category, description)
        randomlist = []
        for i in range(0, 6):
            n = random.randint(0, 9)
            randomlist.append(str(n))
        id = ''.join(randomlist)

        newWork = Work.objects.create(id=id, title=title, maxamount=amount,
                                      maxdays=days, category=category, description=description, creator=data)
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
    option = checksession(request)

    if request.method == "GET":
        search = request.GET.get('q')     # do some research what it does

        status1 = WorkerProfile.objects.filter(pincode__icontains=search)
        workerObj = status1

        if workerObj.count() == 0:
            status2 = WorkerProfile.objects.filter(
                occupation__icontains=search)
            workerObj = status2

        if workerObj.count() == 0:
            status2 = WorkerProfile.objects.filter(address__icontains=search)
            workerObj = status2

        if workerObj.count() == 0:
            print("hi")
            listD = list(search)
            print(list(search.split(" ")))

            userList = User.objects.filter(first_name__icontains=listD[0])
            print(userList)
            status2 = WorkerProfile.objects.filter(username__in=userList)
            workerObj = status2

        if workerObj.count() == 0:
            userList = User.objects.filter(last_name__icontains=listD[1])
            print(userList)
            status2 = WorkerProfile.objects.filter(username__in=userList)
            workerObj = status2

        return render(request, 'app/worker/searchworker.html', {'workerObj': workerObj , 'option': option})
    else:
        print('hi')


def workDescription(request, id):
    option = checksession(request)

    workObj = Work.objects.get(id=id)

    try:
        userObj = User.objects.get(username=request.session['username'])
        workerProfile = WorkerProfile.objects.get(username=userObj)
        print(workerProfile)
    except:
        workerProfile = None

    # Bid Place
    response = Bid.objects.filter(worker=workerProfile, work=workObj)
    print(response)

    if len(response) == 0:
        print(response.count())
        bid = False
        bidData = None
    else:
        bidData = Bid.objects.get(worker=workerProfile, work=workObj)
        print(bidData)
        bid = True

    if request.method == 'POST':
        bidamount = request.POST.get('bidamount')
        biddays = request.POST.get('biddays')
        print(bidamount, biddays)

        newBid = Bid.objects.create(
            worker=workerProfile, work=workObj, proposal_price=bidamount, proposal_days=biddays)
        # newBid.save()

        return redirect('workDescription', id=id)

    return render(request, 'app/user/workDescription.html', {'obj': workObj, 'option': option, 'bid': bid, 'workerProfile': workerProfile, 'bidData': bidData})


def workDelete(request, id):
    obj = Work.objects.get(id=id)
    obj.delete()

    return redirect('myworks')


def workEdit(request, id):
    option = checksession(request)
    obj = Work.objects.get(id=id)
    print(obj.creator.username, request.user)

    if request.method == "POST":

        title = request.POST.get('work_name')
        amount = request.POST.get('amount', None)
        days = request.POST.get('days', None)
        category = request.POST.get('occupation')
        description = request.POST.get('description')
        print(title, amount, days, category, description)

        obj.title = title
        obj.maxamount = amount
        obj.maxdays = days
        obj.description = description
        obj.category = category
        obj.save()
        return redirect('myworks')

    elif obj.creator.username == request.user:
        return render(request, 'app/user/workEdit.html', {'option': option, 'obj': obj})

    else:
        return HttpResponse("Don't be smart !!!")


def workBids(request, id):
    option = checksession(request)
    obj = Work.objects.get(id=id)
    if obj.creator.username == request.user:
        bids = Bid.objects.filter(work=obj, isassigned=True)
        print(bids)
        if len(bids) >= 1:
            print("Assigned")
            # return HttpResponse('Assigned')
            return render(request, 'app/user/workBids.html', {'option': option, 'obj': obj, 'bids': bids, 'msg': 'Assigned'})

        else:
            bids = Bid.objects.filter(work=obj)
            return render(request, 'app/user/workBids.html', {'option': option, 'obj': obj, 'bids': bids})

    else:
        return HttpResponse("Don't be smart !!!")


def workAssign(request, id):
    obj = Bid.objects.get(id=id)
    obj.isassigned = True
    id = obj.work.id
    print(id)
    msgFormat = '\n\n\nCongratulations ' + str(obj.worker.username.first_name) + ' ' + str(obj.worker.username.last_name)  + ' !!! \nYou have assigned a work with details : \n' + 'Work Creator : ' + str(obj.work.creator.username.first_name) + ' ' + str(obj.work.creator.username.last_name) + '\n' + 'Price : Rs.' + str(obj.proposal_price) + '\nDays : ' + str(obj.proposal_days) + '\nAssigned on : ' + str(today)

    message = client.messages.create(
        body=msgFormat, from_='+13362838190', to='+919140562195')
    print(message.sid)

    obj.save()
    return redirect('workBids', id=id)

def workReview(request, id):
    bidObj =  Bid.objects.get(id=id)
    obj = Work.objects.get(id=bidObj.work.id)

    if request.method == 'POST':
        rating = request.POST['rating']
        feedback = request.POST['feedback']
        print(rating, feedback)
        ratingObj = Rating.objects.create(work=obj, rating=rating, feedback=feedback)
        ratingObj.save()
        return redirect('myworks')

    return render(request, 'app/user/review.html',{'obj':obj})
