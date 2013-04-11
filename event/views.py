from accounts.models import UserProfile
from datetime import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from taggit.managers import TaggableManager
from django.shortcuts import render_to_response, redirect
from django.template import Context, loader, RequestContext
from event.models import Event, Comment

def index(request):
    template_var = {}
    try:
        event_list = Event.objects.all().order_by('id')
    except Event.DoesNotExist:
        raise Http404
    output = ', '.join([e.title for e in event_list])    
    template_var["events"] = output	
    return render_to_response("event/index.html", template_var)


def archives(request):
    template_var = {}
    try:
        template_var["events"] = Event.objects.all().order_by("-created")
    except Event.DoesNotExist:
        raise Http404
    return render_to_response("event/event_listview.html", template_var)


def tagpage(request, tag):
	events = Event.objects.filter(tags__name = tag)
	return render_to_response("event/tag_single.html", {"events":events, "tag":tag})

	
def add_comment(request, pk):
    print pk;
    template_var = {}
    p = request.POST
    
    if p.has_key("content") and p["content"]:
        if request.user.is_authenticated():
            comment = Comment(event=Event.objects.get(id=pk))
            comment.user = UserProfile.objects.filter(django_user=request.user)[0]
            comment.content = p["content"]
            comment.save()
    
    return redirect('index')
    

def post(request):
    template_var = {}
    if request.method=="POST":
        title_ = request.POST["title"]
        body_ =  request.POST["body"]
        refer_ = request.POST["refer"]
        tags_ = TaggableManager()
        image1_ = request.FILES["picture"]

    
        event = Event(title = title_, body= body_, refer = refer_, created = "1999-11-12", image1 = image1_)
        event.save()
        return HttpResponseRedirect(reverse("index"))    

    return render_to_response("event/event_post.html",template_var,context_instance=RequestContext(request))
