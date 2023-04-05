from django.shortcuts import render
from django.http import HttpResponse
from mysite import models

def index(request):
    posts=models.Post.objects.filter(enabled=True).order_by('-pub_time')[:30]
    moods=models.Mood.objects.all()
    try:
        user_id=request.GET['user_id']
        user_pass=request.GET['user_pass']
        user_post=request.GET['user_post']
        user_mood=request.GET['mood']
    except:
        user_id = None
        message='若要張貼訊息，請確認已經填寫所有欄位'
    if user_id != None:
        mood=models.Mood.objects.get(status=user_mood)
        post=models.Post.objects.create(mood=mood, nickname=user_id, del_pass=user_pass, message=user_post)
        post.save()
        message='成功存取，請記得編輯密碼[{}]，訊息審查過後會顯示。'.format(user_pass)
    return render(request,'index.html',locals())

def show(request):
    show_post=models.Post.objects.filter(nickname='sss').order_by('pub_time')
    return render(request, 'show.html', locals())

# Create your views here.
def get_example(request):
    # 如果有就get
    try:
        urid=request.GET['user_id']
        urpass = request.GET['user_pass']
        se_byear=request.GET['byear']
        se_month=request.GET['bmonth']
        se_day  =request.GET['bday']
        urfmedia=request.GET.getlist('fmedia')
        locations=request.GET['location']
    #若是沒有，回傳NONE
    except:
        urid=None

    verified = urid is not None and urpass == '12345' or False
    #if urid != None and urpass =='12345':
    #    verified = True
    #else:
    #    verified = False
    years = range(1911, 2031)#不含2031
    mns   = range(1,      13)#不含13
    days  = range(1,      32)#不含32

    return render(request, 'get_example.html', locals())

