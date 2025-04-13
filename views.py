import datetime

# from PIL import Image
from PIL import Image
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
#


# Create your views here.
from myapp.models import *


def login(request):
    return render(request, 'loginindex.html')

def login_post(request):
    username=request.POST['textfield']
    password=request.POST['textfield2']
    re=Login.objects.filter(username=username,password=password)
    if re.exists():
        ree=Login.objects.get(username=username,password=password)
        request.session['lid']=ree.id
        if ree.type == "admin":
            return HttpResponse('''<script>alert("Login Successfull!");window.location='/myapp/home/'</script>''')

        else:
            return HttpResponse('''<script>alert("Invalid User!!!");window.location='/myapp/login/'</script>''')
    else:
        return HttpResponse('''<script>alert("Invalid Username or Password!!");window.location='/myapp/login/'</script>''')

def forgotpw(request):
    return render(request, 'forgot password.html')

def forgotpw_post(request):
    username = request.POST['textfield']
    return HttpResponse("success")


def home(request):
    return render(request,'homeindex.html')


def changepw(request):
    return render(request, 'change password.html')

def changepw_post(request):
    currentpassword = request.POST['textfield']
    newpassword = request.POST['textfield2']
    confirmpassword = request.POST['textfield3']
    pa=Login.objects.filter(id=request.session['lid'],password=currentpassword)
    if pa.exists():
        if newpassword==confirmpassword:
            pa = Login.objects.filter(id=request.session['lid'], password=currentpassword).update(password=confirmpassword)
            return HttpResponse('''<script>alert("Password Updated Successfully!!!!");window.location='/myapp/login/'</script>''')
        else:
            return HttpResponse('''<script>alert("Invalid Password!!");window.location='/myapp/changepw/'</script>''')
    else:
        return HttpResponse('''<script>alert("User not Found");window.location='/myapp/changepw/'</script>''')

def viewuserdetails(request):
    vi=User.objects.all()
    return render(request, 'View user details.html',{"data":vi})

def viewuserdetails_post(request):
    search=request.POST['textfield']
    vi = User.objects.filter(username__icontains=search)
    return render(request, 'View user details.html', {"data": vi})


def viewcomplaints(request):
    cc = Complaints.objects.all()
    return render(request, 'view complaint.html',{"data":cc})

# def viewcomplaints_post(request):
#     fromdate=request.POST['textfield']
#     todate=request.POST['textfield2']
#     searchuser=request.POST['textfield3']
#     if searchuser=='':
#         cc = Complaints.objects.filter(date__range=[fromdate,todate])
#     if fromdate and todate=='':
#         cc = Complaints.objects.filter(USER__email__icontains=searchuser)
#     else:
#         cc = Complaints.objects.filter(date__range=[fromdate,todate],USER__email__icontains=searchuser)
#
#     return render(request, 'view complaint.html', {"data": cc})




from django.shortcuts import render
from .models import Complaints


def viewcomplaints_post(request):
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']
    searchuser = request.POST['textfield3']
    if searchuser == '' and fromdate != '' and todate != '':
        cc = Complaints.objects.filter(date__range=[fromdate, todate])
    elif fromdate == '' and todate == '' and searchuser != '':
        cc = Complaints.objects.filter(USER__email__icontains=searchuser)
    else:
        cc = Complaints.objects.filter(date__range=[fromdate, todate], USER__email__icontains=searchuser)

    return render(request, 'view complaint.html', {"data": cc})


def sendreply(request,cid):
    return render(request, 'send reply.html',{"cid":cid})
def sendreply_post(request):
    reply=request.POST['textfield']

    cid=request.POST['cid']
    res=Complaints.objects.filter(id=cid).update(reply=reply,status="replied")
    return redirect('/myapp/viewcomplaints/')
def viewreview(request):
    rr = Review.objects.all()
    return render(request, 'app review & rating.html',{"data": rr})
def viewreview_post(request):
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']
    rr = Review.objects.filter(date__range=[fromdate, todate])
    return render(request, 'app review & rating.html',{"data":rr})



def adviewcomments(request):
    ad=Comments.objects.filter(Q(type='toxic') | Q(type='warning'))
    return render(request,'view comments.html',{'data':ad})


def blockuser(request,id,pid,cid):
    Request.objects.filter(Q(FROM__id=id,TO__id=pid) | Q(FROM__id=pid,TO__id=id)).delete()
    Comments.objects.filter(id=cid).delete()
    return HttpResponse('''<script>alert("Removed");window.location='/myapp/adviewcomments/'</script>''')


# -------------------------user----------------------


def user_register(request):
    name =request.POST['firstname']
    # lastname =request.POST['lastname']
    email =request.POST['email']
    dob =request.POST['dateofbirth']
    place =request.POST['country']
    gender =request.POST['gender']
    phone =request.POST['phonenumber']
    image =request.POST['image']
    bio =request.POST['pin']
    password=request.POST['password']
    confirmpassword=request.POST['confirmpassword']

    import datetime
    import base64

    #
    date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    a = base64.b64decode(image)
    fh = open("C:\\Users\\KHALE\\Music\\PROJECT\\cyberbullyingdetection\\media\\" + date + ".jpg", "wb")
    # fh = open("C:\\Users\\91815\\PycharmProjects\\cyber\\media\\" + date + ".jpg", "wb")
    path = "/media/" + date + ".jpg"
    fh.write(a)
    fh.close()

    if Login.objects.filter(username=email).exists():
        return JsonResponse({'status': 'no'})


    lobj=Login()
    lobj.username=email
    lobj.password=confirmpassword
    lobj.type='user'
    lobj.save()

    uobj=User()
    uobj.username=name
    uobj.email=email
    uobj.phone=phone
    uobj.photo=path
    uobj.bio=bio
    uobj.place=place
    uobj.gender=gender
    uobj.dob=dob
    uobj.LOGIN_id=lobj.id
    uobj.save()

    return JsonResponse({'status': 'ok'})


def user_login(request):
    username = request.POST['username']
    password = request.POST['password']
    log = Login.objects.filter(username=username, password=password)
    if log.exists():
        obj = Login.objects.get(username=username, password=password)
        if obj.type == 'user':
            lid = obj.id


            return JsonResponse({'status': 'ok','lid':str(lid)})

        if obj.type=='block':
            return JsonResponse({'status': 'no'})


        else:
            return JsonResponse({'status': 'not ok'})
    else:
            return JsonResponse({'status': 'not ok'})

def user_viewprofile(request):
    lid=request.POST['lid']
    data=User.objects.get(LOGIN_id=lid)
    return JsonResponse({'status': 'ok',
                         'name':data.username,
                         'email':data.email,
                         'phone':data.phone,
                         'image':data.photo,
                         'pin':data.bio,
                         'post':"",
                         'place':data.place,
                         'gender':data.gender,
                         'dob':data.dob,
                         'account_type':data.account_type,
                         })


def add_public_account(request):
    lid=request.POST['lid']
    User.objects.filter(LOGIN_id=lid).update(account_type='public')
    return JsonResponse({'status': 'ok'})



def add_private_account(request):
    lid=request.POST['lid']
    User.objects.filter(LOGIN_id=lid).update(account_type='private')
    return JsonResponse({'status': 'ok'})


def user_viewprofileandeditprofile(request):
    lid =request.POST['lid']
    name =request.POST['name']
    gender =request.POST['gender']
    email =request.POST['email']
    phone =request.POST['phone']
    pin =request.POST['pin']
    post =request.POST['post']
    # place =request.POST['place']
    dob =request.POST['dob']
    image = request.POST['image']

    if Login.objects.filter(username=email).exclude(id=lid):
        return JsonResponse({'status': 'no'})

    import datetime
    import base64

    l=Login.objects.get(id=lid)
    l.username=email
    l.save()



    obj=User.objects.get(LOGIN_id=lid)

    if len(image)>0 :

       date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
       a = base64.b64decode(image)
       fh = open("C:\\Users\\KHALE\\Music\\PROJECT\\cyberbullyingdetection\\media\\" + date + ".jpg", "wb")
       # fh = open("C:\\Users\\91815\\PycharmProjects\\cyber\\media\\" + date + ".jpg", "wb")
       path = "/media/" + date + ".jpg"
       fh.write(a)
       fh.close()
       obj.photo = path

    obj.username=name
    obj.email=email
    obj.phone=phone
    obj.post=post
    obj.bio=pin
    obj.gender=gender
    obj.dob=dob
    obj.save()

    return JsonResponse({'status': 'ok'})

def user_chnagepassword(request):
    oldpassword = request.POST['oldpassword']
    newpassword = request.POST['newpassword']
    confirmpassword = request.POST['confirmpassword']
    lid = request.POST['lid']
    a = Login.objects.filter(id=lid, password=oldpassword)
    if a.exists():
        a = Login.objects.get(id=lid, password=oldpassword)

        if newpassword == confirmpassword:
            b = Login.objects.filter(id=lid).update(password=confirmpassword)
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'not ok'})
    else:
        return JsonResponse({'status': 'not ok'})


# def user_addpost(request):
#     newpost =request.POST['newpost']
#     caption=request.POST['caption']
#     lid=request.POST['lid']
#
#     import datetime
#     import base64
#
#     #
#     date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
#     a = base64.b64decode(newpost)
#     fh = open("C:\\Users\\SHIBILA\\.PyCharm2017.1\\media\\userpost\\" + date + ".jpg", "wb")
#     # fh = open("C:\\Users\\91815\\PycharmProjects\\cyber\\media\\" + date + ".jpg", "wb")
#     path = "/media/userpost/" + date + ".jpg"
#     fh.write(a)
#     fh.close()
#
#     # import datetime
#     # import base64
#     # #
#     # date = "post/"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+'jpg'
#     # a = base64.b64decode(newpost)
#     # open(r'C:\\Users\\SHIBILA\\.PyCharm2017.1\\media\\post\\'+date+'wb').write(a)
#     #
#     # # fh = open(r"C:\\Users\\SHIBILA\\.PyCharm2017.1\\media\\post\\" + date + ".jpg", "wb")
#     # # fh = open("C:\\Users\\91815\\PycharmProjects\\cyber\\media\\" + date + ".jpg", "wb")
#     # path = "/media/post/" + date + ".jpg"
#     # fh
#     # fh.close()
#
#     obj=uploadpost()
#     obj.USER=User.objects.get(LOGIN_id=lid)
#     obj.post=path
#     obj.caption=caption
#     from datetime import datetime
#     obj.date=datetime.now()
#     obj.save()
#     return JsonResponse({'status': 'ok'})
#





def useraddpost(request):
    newpost=request.POST['newpost']
    caption=request.POST['caption']
    loc=request.POST['loc']
    lid=request.POST['lid']
    import datetime
    import base64

    dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+'.bmp'
    a = base64.b64decode(newpost)
    path = "/media/post/" + dt
    with open("C:\\Users\\KHALE\\Music\\PROJECT\\cyberbullyingdetection\\media\\post\\" + dt, "wb") as f:
        f.write(a)
        f.close()

    from datetime import datetime
    date = datetime.now().strftime('%Y-%m-%d')
    obj = Post()
    obj.photo = path
    obj.location = loc
    obj.caption = caption
    obj.date = date

    obj.USER = User.objects.get(LOGIN_id=lid)
    obj.save()

    u = User.objects.all()
    uids = []
    imgs = []

    import face_recognition

    mediapth = "C:\\Users\\KHALE\\Music\\PROJECT\\cyberbullyingdetection\\media\\"

    for i in u:

        if str(i.LOGIN_id) == str(lid):
            pass
        else:

            uids.append(i.id)

            # print(mediapth + i.photo.replace("/media/", ""))
            try:
                picture_of_me = face_recognition.load_image_file(mediapth + i.photo.replace("/media/", ""))
                my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

                imgs.append(my_face_encoding)

                print("added")
            except Exception as e:

                print("errrrr", e)
                pass
    #
    unknownfacesimages = "C:\\Users\\KHALE\\Music\\PROJECT\\cyberbullyingdetection\\media\\post\\" + dt

    picture_of_me = face_recognition.load_image_file(unknownfacesimages)
    my_face_encoding = face_recognition.face_encodings(picture_of_me)
    #
    # print(len(my_face_encoding))
    #
    import cv2
    img = face_recognition.load_image_file(unknownfacesimages)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(img_rgb)
    # g = 1
    # for top, right, bottom, left in face_locations:
    #     # Draw a box around the face
    #     cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
    #
    #     crop_img = img_rgb[top:bottom, left:right]
    #     cv2.imwrite(str(g) + 'test_crop.png', crop_img)
    #
    #     g = g + 1


    from PIL import Image
    # Open an image
    imagenews = Image.open(unknownfacesimages)
    width, height = imagenews.size
    new_image = Image.new("RGB", (width, height))

    def modify_pixel(pixel):
        return (pixel[0] ^ 124, pixel[1] ^ 178, pixel[2] ^ 167)

    m = 0
    for i in my_face_encoding:
        print(face_locations[m])
        top, right, bottom, left = face_locations[m]
        cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)

        s = face_recognition.compare_faces(imgs, i, tolerance=0.45)
        print(s)

        for i in range(len(s)):
            if s[i] == True:

                p = Notifications()
                p.POST = obj
                p.USER_id = uids[i]
                p.status = "pending"
                p.date = datetime.now().date()
                p.time = datetime.now().time()
                p.bottom = bottom
                p.left = left
                p.right = right
                p.top = top
                p.save()

                crop_img = img_rgb[top:bottom, left:right]

                for x in range(left, right):
                    for y in range(top, bottom):
                        pixel = imagenews.getpixel((x, y))
                        new_pixel = modify_pixel(pixel)
                        imagenews.putpixel((x, y), new_pixel)

        m = m + 1

    imagenews.save("C:\\Users\\KHALE\\Music\\PROJECT\\cyberbullyingdetection\\media\\post\\" + dt)

    return JsonResponse({"status": "ok"})

    # import face_recognition
    #
    #
    # data=User.objects.all().exclude(LOGIN_id=lid)
    # lids=[]
    # photoslandmarks=[]
    #
    #
    # for i in range(0,len(data)):
    #
    #
    #     p="C:\\Users\\KHALE\\Music\\PROJECT\\cyberbullyingdetection\\media\\"
    #
    #     pp= data[i].photo.replace("/media/","")
    #
    #     fullpath=p+pp
    #
    #     print(fullpath)
    #     l=data[i].LOGIN.id
    #
    #     image = face_recognition.load_image_file(fullpath)
    #     face_landmarks_list = face_recognition.face_encodings(image)
    #
    #     print(face_landmarks_list)
    #
    #     photoslandmarks.append(face_landmarks_list)
    #     lids.append(l)
    #
    # otherphotos="C:\\Users\\KHALE\\Music\\PROJECT\\cyberbullyingdetection\\media\\post\\" + dt
    # image= face_recognition.load_image_file(otherphotos)
    # face_landmarks_list = face_recognition.face_encodings(image)
    #
    # print(len(face_landmarks_list))
    #





















    #
    #
    #
    # from datetime import datetime
    # date = datetime.now().strftime('%Y-%m-%d')
    # obj = Post()
    # obj.photo = path
    # obj.caption = caption
    # obj.date = date
    # obj.location = loc
    # obj.USER=User.objects.get(LOGIN_id=lid)
    # obj.save()
    # return JsonResponse({"status": "ok"})








def user_viewothersusers_post(request):
    lid=request.POST['lid']
    name= request.POST["name"]
    res=User.objects.filter(name__icontains=name).exclude(LOGIN_id=lid)
    l=[]
    for i in res:
           l.append({'id':i.id,'name':i.username,'image':i.photo,'gender':i.gender})
    print(l)
    return JsonResponse({'status': 'ok','data':l})




def user_viewothersusers(request):
    lid=request.POST['lid']
    res=User.objects.exclude(LOGIN=lid)
    l=[]
    for i in res:

           if Request.objects.filter(FROM__LOGIN_id=lid,TO__LOGIN_id=i.LOGIN.id).exists():
               pass
           elif Request.objects.filter(TO__LOGIN_id=lid,FROM__LOGIN_id=i.LOGIN.id).exists():
               pass
           else:
               l.append({'id':i.id,'name':i.username,'image':i.photo,'gender':i.gender,})
    print(l)
    return JsonResponse({'status': 'ok','data':l})

def user_sendfriendrequest(request):
    lid=request.POST['lid']
    uid=request.POST['uid']
    re=Request.objects.filter(TO=uid,FROM__LOGIN_id=lid) | Request.objects.filter(FROM=uid,TO__LOGIN_id=lid)
    if re.exists():
        return JsonResponse({'status':'no'})
    else:
        r=Request()
        r.FROM = User.objects.get(LOGIN=lid)
        r.TO = User.objects.get(pk=uid)
        from datetime import datetime
        r.date = datetime.now().today()
        r.time = datetime.now().time()
        r.status = 'pending'
        r.save()
        return JsonResponse({'status': 'ok'})


def user_viewotherspost(request):
    l = []
    lid = request.POST['lid']

    # friend_ids = Request.objects.filter((Q(FROM__LOGIN_id=lid) | Q(TO__LOGIN_id=lid)),status='accepted').values_list('FROM_id', 'TO_id')
    #
    # friend_ids = set([uid for pair in friend_ids for uid in pair])

    res = Post.objects.all() #.filter(USER__id__in=friend_ids).exclude(USER__LOGIN_id=lid)

    for post in res:
        liked = 'yes' if Like.objects.filter(USER__LOGIN_id=lid, POST_id=post.id).exists() else 'no'
        lcnt = Like.objects.filter(POST_id=post.id).count()

        l.append({
            'id': post.id,
            'date': post.date,
            'post': post.photo,
            'name': post.USER.username,
            'loc': post.location,
            'cap': post.caption,
            'image': post.USER.photo,
            'liked': liked,
            'likes': str(lcnt)
        })

    return JsonResponse({'status': 'ok', 'data': l})


def user_viewownpost(request):
    lid=request.POST['lid']
    res=Post.objects.filter(USER__LOGIN_id=lid)
    l=[]
    for i in res:
        liked = 'no'
        lcnt = Like.objects.filter(POST_id=i.id)

        if Like.objects.filter(USER__LOGIN_id=lid, POST_id=i.id).exists():
            liked = 'yes'
        l.append({'id':i.id,'date':i.date,'post':i.photo,'caption':i.caption,'loc':i.location,'name':i.USER.username,'image':i.USER.photo,'likes': str(len(lcnt))})
    return JsonResponse({'status': 'ok','data':l})

def user_viewotherpost(request):
    lid=request.POST['lid']
    res=Post.objects.filter(USER__account_type='public')
    l=[]
    for i in res:
        liked = 'no'
        lcnt = Like.objects.filter(POST_id=i.id)

        if Like.objects.filter(POST_id=i.id).exists():
            liked = 'yes'
        l.append({'id':i.id,'date':i.date,'post':i.photo,'caption':i.caption,'loc':i.location,'name':i.USER.username,'image':i.USER.photo,'likes': str(len(lcnt))})
    return JsonResponse({'status': 'ok','data':l})









def user_viewapprovedrequest(req):
    lid=req.POST['lid']
    var=Request.objects.filter(status='accepted',FROM__LOGIN_id=lid)
    l=[]
    for i in var:
        l.append({'id':i.id,'date':i.date,'Status':i.status,'name':i.FROM.name})
    print(l)
    return JsonResponse({'status': 'ok','data':l})


def user_viewfriedrequest(requestS):
    lid=requestS.POST['lid']
    res = Request.objects.filter(TO__LOGIN_id=lid,status="pending")
    l = []
    for i in res:
        l.append({'id': i.id, 'name': i.FROM.username, 'image': i.FROM.photo, 'gender': i.FROM.gender,'status': i.status })
    print(lid)
    return JsonResponse({'status': 'ok', 'data': l})


def user_viewreject(request):
    rid=request.post['rid']
    var=Request.objects.filter(id=rid).update(status='rejected')
    return JsonResponse({'status': 'ok'})


def viewfriends(request):
    lid = request.POST['lid']
    l = Login.objects.get(id=lid)
    print(l, 'llll')
    uid = User.objects.get(LOGIN_id=l)
    print(uid, 'uuuu')

    roj = Request.objects.filter(FROM_id=uid,status='accepted') | Request.objects.filter(TO_id=uid,status='accepted')
    print(roj,'rrrrrrrr')
    user_data = []
    for user in roj:
        if user.TO.id == uid.id:
            user_data.append({
                "image": user.FROM.photo,
                "id": user.id,
                "name": user.FROM.username,
                "ulid": user.FROM.LOGIN_id,
                "gender": user.FROM.gender,
            })
        if user.FROM.id == uid.id:
            user_data.append({
                "image": user.TO.photo,
                "id": user.id,
                "gender": user.TO.gender,
                "ulid": user.TO.LOGIN_id,
                "name": user.TO.username,
            })

    return JsonResponse({"status": "ok", 'data': user_data})




def user_viewfriedlist(requests):
    lid=requests.POST['lid']
    res=Request.objects.filter( Q(TO__LOGIN_id=lid)|Q(FROM__LOGIN_id=lid),status='accepted')
    l=[]
    for i in res:
        l.append({'id': i.id, 'name': i.FROM.username, 'image': i.FROM.photo, 'gender': i.FROM.gender,'status': i.status })
    return JsonResponse({'status': 'ok', 'data': l})


def user_viewcomments(request):
    res=Comments.objects.filter(type='normal')
    l=[]
    for i in res:
        l.append({'id':i.id,'userid':i.USER.id,'uploadpost':i.POST.id , 'comment':i.comment,'date':i.date})
    return JsonResponse({'status': 'ok','data':l})


def user_viewcommentsandreply(request):
    pid=request.POST['pid']
    res=Comments.objects.filter(POST_id=pid,type='normal')
    l=[]
    for i in res:
        l.append({'id':i.id,'userid':i.USER.username,'userphoto':i.USER.photo,'uploadpost':i.POST.id , 'comment':i.comments,'date':i.date})
    return JsonResponse({'status': 'ok','data':l})

def user_addcomment(request):
    lid = request.POST['lid']
    pid = request.POST['postid']

    comments=request.POST['comment']

    from transformers import pipeline

    # Load the pre-trained model for sentiment analysis
    classifier = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')

    # Function to detect toxic comments
    def detect_toxic_comment(comment):
        result = classifier(comment)[0]
        label = result['label']
        score = result['score']

        if label == 'NEGATIVE' and score > 0.7:  # Adjust the threshold as needed
            return "Toxic"
        else:
            return "Non-Toxic"

    mm=detect_toxic_comment(comments)

    print(mm)

    if mm == 'Non-Toxic':
        b = "normal"
        print(b)
        obj = Comments()
        obj.USER = User.objects.get(LOGIN_id=lid)
        obj.POST_id = pid
        obj.comments = comments
        obj.date = datetime.datetime.now().date()
        obj.time = datetime.datetime.now().time()
        obj.type=b
        obj.save()
        return JsonResponse({'status': 'ok'})
    else:
        b = "toxic"
        print(b)

        g = Comments.objects.filter(USER__LOGIN=lid, type="warning")

        if len(g) >= 6:  # Check directly against the integer
            User.objects.filter(LOGIN=lid).update(status="block")
            Login.objects.filter(id=lid).update(type='block')
            return JsonResponse({'status': 'blocked'})
        else:
            obj = Comments()
            obj.USER = User.objects.get(LOGIN_id=lid)
            obj.POST_id = pid
            obj.comments = comments
            obj.date = datetime.datetime.now().date()
            obj.time = datetime.datetime.now().time()
            obj.type = "warning"
            obj.save()
            return JsonResponse({'status': 'no'})



        obj = Comments()
        obj.USER = User.objects.get(LOGIN_id=lid)
        obj.POST_id = pid
        obj.comments = comments
        obj.date = datetime.datetime.now().date()
        obj.time = datetime.datetime.now().time()
        obj.type = "warning"
        obj.save()

        category=["defame","identity_hate","privacy_violate","obscene","sexually_explicit"]

        categorycontent=["Section 500  of the Indian Penal Code","Section 66C of the Information Technology Act","Section 66 E of IT Act","Section 67 of IT Act","Section 67A of IT Act"]

        defame=["",""]
        identity_hate=[]
        privacy_violate=[]
        obscene=[]
        sexually_explicit=[]

        punishment=[]

        return JsonResponse({'status': 'warning'})






def user_viewreply(request):
    lid=request.POST['lid']
    r=Complaints.objects.filter(USER__LOGIN_id=lid)
    l=[]
    for i in r:
        l.append({'id':i.id,'date':i.date,'complaint':i.complaints,'reply':i.reply ,'status':i.status})

    return JsonResponse({'status': 'ok','data':l})


def user_sendcomplaint(request):
    lid = request.POST['lid']
    date=datetime.date.today()
    complaints=request.POST['complaint']
    reply='pending'
    status='pending'

    obj=Complaints()
    obj.USER=User.objects.get(LOGIN_id=lid)
    obj.date=date
    obj.complaints=complaints
    obj.reply='pending'
    obj.status=status
    obj.save()

    return JsonResponse ({'status':'ok'})
def and_review_rating(request):
    lid = request.POST['lid']
    date=datetime.date.today()
    re=request.POST['review']
    ra=request.POST['rating']

    obj=Review()
    obj.USER=User.objects.get(LOGIN_id=lid)
    obj.date=date
    obj.review=re
    obj.rating=ra
    obj.save()

    return JsonResponse ({'status':'ok'})

def user_chatfromfrieds(request):
        return JsonResponse ({'status':'ok'})

def user_followback(request):
    lid = request.POST['lid']
    uid = request.POST['uid']
    re = Request.objects.filter(TO=uid, FROM__LOGIN_id=lid)
    if re.exists():
        return JsonResponse({'status': 'no'})
    else:
        re = Request.objects.filter(id=uid).update(status='accepted')
        return JsonResponse({'status': 'ok'})



def user_remove(request):
        uid = request.POST['uid']
        re = Request.objects.filter(id=uid).delete()
        return JsonResponse({'status': 'ok'})

def user_fromremovefromfriendlist(request):
        uid = request.POST['uid']
        print(uid)
        re = Request.objects.get(id=uid).delete()
        return JsonResponse({'status': 'ok'})


def postremove(request):
    uid = request.POST['uid']
    re = Post.objects.filter(id=uid).delete()
    return JsonResponse({'status': 'ok'})

def chat_send(request):
    FROM_id=request.POST['from_id']
    TOID_id=request.POST['to_id']
    msg=request.POST['message']

    from  datetime import datetime
    c=Messagechat()
    c.FROM_id=FROM_id
    c.TO_id=TOID_id
    c.message=msg
    c.date=datetime.now().date()
    c.time=datetime.now().time()
    c.save()
    return JsonResponse({'status':"ok"})

def chat_view_and(request):
    from_id=request.POST['from_id']
    to_id=request.POST['to_id']
    l=[]
    data1=Messagechat.objects.filter(FROM_id=from_id,TO_id=to_id).order_by('id')
    data2=Messagechat.objects.filter(FROM_id=to_id,TO_id=from_id).order_by('id')

    data= data1 | data2
    print(data)

    for res in data:
        l.append({'id':res.id,'from':res.FROM.id,'to':res.TO.id,'msg':res.message,'date':res.date})

    return JsonResponse({'status':"ok",'data':l})

def likes(request):
    lid=request.POST['lid']
    pid=request.POST['pid']
    obj=Like()
    if Like.objects.filter(USER__LOGIN_id=lid,POST_id=pid).exists():
        Like.objects.filter(USER__LOGIN_id=lid, POST_id=pid).delete()
        return JsonResponse({'status': "ok"})

    obj.USER=User.objects.get(LOGIN_id=lid)
    obj.POST_id=pid
    obj.date=datetime.datetime.now().date()
    obj.time=datetime.datetime.now().time()
    obj.save()

    return JsonResponse({'status':"ok"})


def user_viewcommentsreply(request):
    cid=request.POST['cid']
    res=Comments.objects.filter(COMMENT_id=cid)
    l=[]
    for i in res:
        l.append({'id':i.id,'userid':i.USER.username,'userphoto':i.USER.photo,'uploadpost':i.COMMENT.id , 'comment':i.reply,'date':i.date,'time':i.time})
    return JsonResponse({'status': 'ok','data':l})

def user_addcommentreply(request):
    lid = request.POST['lid']
    cid = request.POST['cid']

    reply=request.POST['reply']
    date=datetime.date.today()


    # obj=CommentReply()
    # obj.USERID=User.objects.get(LOGIN_id=lid)
    # obj.COMMENT_id=cid
    # obj.reply=reply
    # obj.date=date
    # obj.time=datetime.datetime.now().strftime('%H:%M:%S')
    # obj.save()

    return JsonResponse({'status': 'ok'})


###################ml




def user_viewnotification(request):
    lid= request.POST["lid"]
    res=Notifications.objects.filter(USER__LOGIN_id=lid,status='pending')
    l=[]

    for i in res:

        l.append({'id':i.id,'date':i.date,'post':i.POST.photo,'name':i.POST.USER.username,'image':i.POST.USER.photo})
    return JsonResponse({'status': 'ok','data':l})


def accept_notification(request):
    nid= request.POST["nid"]
    Notifications.objects.filter(id=nid).update(status='approved')
    n=Notifications.objects.get(id=nid).POST.photo
    pid=Notifications.objects.get(id=nid).POST.id
    print(n)
    bottom=int(Notifications.objects.get(id=nid).bottom)
    left=int(Notifications.objects.get(id=nid).left)
    right=int(Notifications.objects.get(id=nid).right)
    top=int(Notifications.objects.get(id=nid).top)
    postimage=Notifications.objects.get(id=nid).POST.photo
    postimage=postimage.replace("/media/post/","")
    imagenews = Image.open("C:\\Users\\KHALE\\Music\\PROJECT\\cyberbullyingdetection\\media\\post\\" + postimage)
    width, height = imagenews.size
    new_image = Image.new("RGB", (width, height))
    def modify_pixel(pixel):
        return (pixel[0] ^ 124, pixel[1] ^ 178, pixel[2] ^ 167)
    for x in range(left, right):
        for y in range(top, bottom):
            pixel = imagenews.getpixel((x, y))
            new_pixel = modify_pixel(pixel)
            imagenews.putpixel((x, y), new_pixel)
    dates= datetime.datetime.now().strftime("%Y%m%d%H%M%f")+".bmp"
    p=Post.objects.get(id=pid)
    imagenews.save("C:\\Users\\KHALE\\Music\\PROJECT\\cyberbullyingdetection\\media\\post\\" + dates)
    p.photo="/media/post/"+ dates
    p.save()
    return JsonResponse({'status': 'ok'})

def reject_notification(request):
    nid= request.POST["nid"]
    Notifications.objects.filter(id=nid).update(status='reject')
    return JsonResponse({'status': 'ok'})


from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, \
    f1_score, RocCurveDisplay
import numpy as np

# def confusionmatrix(request):
#     # Load the dataset
#     import os
#     import time
#     import numpy as np
#     import pandas as pd
#     import re
#
#     import keras
#     from keras import layers, optimizers
#     from keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout
#     from keras.models import Model
#     from keras.preprocessing.text import Tokenizer
#     from keras.preprocessing.sequence import pad_sequences
#
#     from sklearn.model_selection import train_test_split
#     from sklearn.metrics import accuracy_score
#
#     import pickle
#     keras.backend.clear_session()
#     sms_df = pd.read_csv(r'C:\Users\afzal\PycharmProjects\cyberbullyingdetection\spamham.csv')
#
#     # Labels and messages
#     labels = sms_df.values[:, 1]
#     msgs = sms_df.values[:, 0]
#
#     # Split dataset
#     train_texts, test_texts, train_labels, test_labels = train_test_split(msgs, labels, test_size=0.1, random_state=500)
#
#     # Tokenization and padding
#     VOCABULARY_SIZE = 5000
#     tokenizer = Tokenizer(num_words=VOCABULARY_SIZE)
#     tokenizer.fit_on_texts(train_texts)
#     MAX_SENTENCE_LENGTH = 100
#     trainFeatures = tokenizer.texts_to_sequences(train_texts)
#     trainFeatures = pad_sequences(trainFeatures, MAX_SENTENCE_LENGTH, padding='post')
#     testFeatures = tokenizer.texts_to_sequences(test_texts)
#     testFeatures = pad_sequences(testFeatures, MAX_SENTENCE_LENGTH, padding='post')
#
#     # Define the model
#     model = Sequential()
#     model.add(Embedding(input_dim=VOCABULARY_SIZE + 1, output_dim=10, input_length=MAX_SENTENCE_LENGTH))
#     model.add(Conv1D(16, 5, activation='relu'))
#     model.add(Dropout(0.5))
#     model.add(GlobalMaxPooling1D())
#     model.add(Dropout(0.5))
#     model.add(Dense(8, activation='relu'))
#     model.add(Dense(1, activation='sigmoid'))
#
#     optimizer = optimizers.Adam(lr=0.001)
#     model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
#
#     # Train the model
#     model.fit(trainFeatures, train_labels, batch_size=32, epochs=20)
#
#     # Predict on test data
#     predictions = model.predict(testFeatures)
#     predicted_labels = [1 if p[0] > 0.6 else 0 for p in predictions]
#
#     # Confusion Matrix and Classification Report
#     cm = confusion_matrix(test_labels, predicted_labels)
#
#     cr = classification_report(test_labels, predicted_labels)
#
#     # Convert confusion matrix and classification report to string
#     cm_str = str(cm)
#     cr_str = str(cr)
#
#     # Pass the results to the template
#     context = {
#         'confusion_matrix': cm_str,
#         'classification_report': cr_str
#     }
#
#     return render(request, 'confusionmatrix.html', context)


#
# from django.shortcuts import render
# import numpy as np
# import pandas as pd
# import keras
# from keras.models import Sequential
# from keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout
# from keras.preprocessing.text import Tokenizer
# from keras.preprocessing.sequence import pad_sequences
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, \
#     f1_score
# import matplotlib.pyplot as plt
# import seaborn as sns
# import io
# import urllib, base64
#
#
# # Ensure that the necessary libraries are installed:
# # pip install matplotlib seaborn
#
# def confusionmatrix(request):
#     # --- Spam/Ham Dataset ---
#     # Load the SMS spam/ham dataset
#     sms_df = pd.read_csv(r'C:\Users\afzal\PycharmProjects\cyberbullyingdetection\spamham.csv')
#
#     # Labels and messages
#     labels = sms_df.values[:, 1]
#     msgs = sms_df.values[:, 0]
#
#     # Check for NaN or unexpected values in the dataset
#     if labels.isnull().any():
#         print("Warning: There are NaN values in the labels.")
#     if msgs.isnull().any():
#         print("Warning: There are NaN values in the messages.")
#
#     # Convert the labels to binary (0 and 1) if needed (ensure there are no unexpected values)
#     labels = labels.apply(lambda x: 1 if x == "spam" else 0)
#
#     # Split dataset for training and testing
#     train_texts, test_texts, train_labels, test_labels = train_test_split(msgs, labels, test_size=0.1, random_state=500)
#
#     # Tokenization and padding for text data
#     VOCABULARY_SIZE = 5000
#     tokenizer = Tokenizer(num_words=VOCABULARY_SIZE)
#     tokenizer.fit_on_texts(train_texts)
#     MAX_SENTENCE_LENGTH = 100
#     trainFeatures = tokenizer.texts_to_sequences(train_texts)
#     trainFeatures = pad_sequences(trainFeatures, MAX_SENTENCE_LENGTH, padding='post')
#     testFeatures = tokenizer.texts_to_sequences(test_texts)
#     testFeatures = pad_sequences(testFeatures, MAX_SENTENCE_LENGTH, padding='post')
#
#     # Define the deep learning model for Spam/Ham classification
#     model = Sequential()
#     model.add(Embedding(input_dim=VOCABULARY_SIZE + 1, output_dim=10, input_length=MAX_SENTENCE_LENGTH))
#     model.add(Conv1D(16, 5, activation='relu'))
#     model.add(Dropout(0.5))
#     model.add(GlobalMaxPooling1D())
#     model.add(Dropout(0.5))
#     model.add(Dense(8, activation='relu'))
#     model.add(Dense(1, activation='sigmoid'))
#
#     # Compile the model
#     optimizer = keras.optimizers.Adam(lr=0.001)
#     model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
#
#     # Train the model on the spam/ham dataset
#     model.fit(trainFeatures, train_labels, batch_size=32, epochs=20)
#
#     # Predict on test data
#     predictions = model.predict(testFeatures)
#     predicted_labels = [1 if p[0] > 0.6 else 0 for p in predictions]
#
#     # Ensure the predicted_labels are binary (0 or 1)
#     predicted_labels = np.array(predicted_labels)
#
#     # Confusion Matrix for Spam/Ham Dataset
#     cm_sms = confusion_matrix(test_labels, predicted_labels)
#
#     # Plot confusion matrix for Spam/Ham dataset
#     plt.figure(figsize=(6, 5))
#     sns.heatmap(cm_sms, annot=True, fmt='g', xticklabels=['Ham', 'Spam'], yticklabels=['Ham', 'Spam'])
#     plt.ylabel('Prediction', fontsize=13)
#     plt.xlabel('Actual', fontsize=13)
#     plt.title('Spam/Ham Confusion Matrix', fontsize=17)
#
#     # Save the plot to a BytesIO object and convert to base64 for embedding in HTML
#     buf = io.BytesIO()
#     plt.savefig(buf, format='png')
#     buf.seek(0)
#     img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
#     buf.close()
#
#     # Metrics for Spam/Ham classification
#     accuracy_sms = accuracy_score(test_labels, predicted_labels)
#     precision_sms = precision_score(test_labels, predicted_labels)
#     recall_sms = recall_score(test_labels, predicted_labels)
#     f1_sms = f1_score(test_labels, predicted_labels)
#
#     print("\nSpam/Ham Classification Metrics:")
#     print(f"Accuracy: {accuracy_sms}")
#     print(f"Precision: {precision_sms}")
#     print(f"Recall: {recall_sms}")
#     print(f"F1-score: {f1_sms}")
#
#     # Classification report (use this for detailed metrics)
#     classification_rep = classification_report(test_labels, predicted_labels)
#
#     # Pass the results to the template
#     context = {
#         'confusion_matrix': str(cm_sms),
#         'classification_report': classification_rep,
#         'accuracy': accuracy_sms,
#         'precision': precision_sms,
#         'recall': recall_sms,
#         'f1_score': f1_sms,
#         'confusion_matrix_image': img_str  # Pass the image as base64
#     }
#
#     return render(request, 'confusionmatrix.html', context)




# def confusion_metrix(request):
#     import warnings
#     def warn(*args, **kwargs):
#         pass
#
#     warnings.warn = warn
#
#     import os
#     import time
#     import numpy as np
#     import pandas as pd
#     import re
#
#     import keras
#     from keras import layers, optimizers
#     from keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout
#     from keras.models import Model
#     from keras.preprocessing.text import Tokenizer
#     from keras.preprocessing.sequence import pad_sequences
#
#     from sklearn.model_selection import train_test_split
#     from sklearn.metrics import accuracy_score, confusion_matrix
#
#     import pickle
#     from keras.models import Sequential
#     import keras.backend as K
#
#     # Clear session to avoid memory issues
#     K.clear_session()
#
#     # Load data
#     sms_df = pd.read_csv(r'C:\Users\afzal\PycharmProjects\cyberbullyingdetection\spamham.csv')
#
#     # Split data into labels and messages
#     labels = sms_df.values[:, 1]
#     msgs = sms_df.values[:, 0]
#
#     # Split dataset into train and test sets
#     train_texts, test_texts, train_labels, test_labels = train_test_split(msgs, labels, test_size=0.1, random_state=500)
#
#     # Prepare tokenizer for text processing
#     VOCABULARY_SIZE = 5000
#     tokenizer = Tokenizer(num_words=VOCABULARY_SIZE)
#     tokenizer.fit_on_texts(train_texts)
#
#     # Maximum sentence length (you can adjust this depending on your dataset)
#     MAX_SENTENCE_LENGTH = 100
#
#     # Tokenize and pad the sequences
#     trainFeatures = tokenizer.texts_to_sequences(train_texts)
#     trainFeatures = pad_sequences(trainFeatures, MAX_SENTENCE_LENGTH, padding='post')
#
#     testFeatures = tokenizer.texts_to_sequences(test_texts)
#     testFeatures = pad_sequences(testFeatures, MAX_SENTENCE_LENGTH, padding='post')
#
#     # Model parameters
#     FILTERS_SIZE = 16
#     KERNEL_SIZE = 5
#     EMBEDDINGS_DIM = 10
#     LEARNING_RATE = 0.001
#     BATCH_SIZE = 32
#     EPOCHS = 20
#
#     # Build the model
#     model = Sequential()
#     model.add(Embedding(input_dim=VOCABULARY_SIZE + 1, output_dim=EMBEDDINGS_DIM, input_length=MAX_SENTENCE_LENGTH))
#     model.add(Conv1D(FILTERS_SIZE, KERNEL_SIZE, activation='relu'))
#     model.add(Dropout(0.5))
#     model.add(GlobalMaxPooling1D())
#     model.add(Dropout(0.5))
#     model.add(Dense(8, activation='relu'))
#     model.add(Dense(1, activation='sigmoid'))
#
#     # Compile the model
#     optimizer = optimizers.Adam(lr=LEARNING_RATE)
#     model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
#
#     # Train the model
#     history = model.fit(trainFeatures, train_labels, batch_size=BATCH_SIZE, epochs=EPOCHS)
#
#     # Save the tokenizer and model weights
#     with open('tokenizer.pickle', 'wb') as handle:
#         pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
#
#     model_json = model.to_json()
#     with open("model.json", "w") as json_file:
#         json_file.write(model_json)
#     model.save_weights("model.h5")
#
#     # Predict on the test set
#     x = model.predict(testFeatures)
#
#     print("Predicted probabilities:", x[:10])  # Check first 10 predicted values
#     predicted = (x > 0.5).astype(int)
#     print("Binary Predictions:", predicted[:10])  # Verify binary conversion
#     print("Test labels:", test_labels[:10])
#     print("Test labels shape:", test_labels.shape)
#
#     predicted = (x > 0.5).astype(int)  # Convert probabilities to binary labels (0 or 1)
#
#
#     print(len(test_labels),"jjjjjj")
#     print(len(predicted),"kkkkkk")
#
#     s=[]
#
#
#     for i in predicted:
#         a=i
#         # print(a[0],"helloiiiiiiii")
#
#         s.append(a[0])
#
#     print(s, "nnn")
#     print(test_labels, "mmmm")
#
#     print(type(s),type(test_labels),"hello")
#
#
#     k=[]
#
#     for i in test_labels:
#         k.append(i)
#
#     cm = confusion_matrix(k, s)
#
#     print(cm)
#     from  sklearn.metrics import  accuracy_score,f1_score, recall_score, precision_score,roc_curve
#     acc=accuracy_score(k,s)
#     f1score=f1_score(k,s)
#     rec=recall_score(k,s)
#     pre=precision_score(k,s)
#     import matplotlib.pyplot as plt
#     fpr, tpr, _ = roc_curve(k, s)
#
#     # Create the RocCurveDisplay object
#     roc_display = RocCurveDisplay(fpr=fpr, tpr=tpr).plot()
#
#     # Save the ROC curve as an image
#     plt.savefig('C:\\Users\\KHALE\\Music\\PROJECT\\cyberbullyingdetection\\media\\roc_curve.png')
#
#
#
#
#
#
#     return render(request,"cnfsn_mtrix.html",{'cf':cm, 'acc':acc, 'f1score': f1score,'rec':rec, 'pre': pre,  })
#
#





