from datetime import date
from django.shortcuts import render
from .models import Project, Owner, Technologies, Languages
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from projects.forms import EditOwnerNickname

# Create your views here.
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_projects = Project.objects.all().count()

    # The 'all()' is implied by default.
    num_owners = Owner.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_projects': num_projects,
        'num_owners': num_owners,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class ProjectListView(generic.ListView):
    model = Project
    paginate_by = 7

class ProjectDetailView(generic.DetailView):
    model = Project

class OwnerListView(generic.ListView):
    model = Owner
    paginate_by = 10

class OwnerDetailView(generic.DetailView):
    model = Owner

@login_required
def edit_owner_nickname(request, pk):
    owner = get_object_or_404(Owner, pk=pk)

    if request.method == 'POST':

        form = EditOwnerNickname(request.POST)

        if form.is_valid():
            owner.nickname = form.cleaned_data['nickname']
            owner.save()

            return HttpResponseRedirect(reverse('owner-detail', args=[str(pk)]))
            
    else:
        proposed_nickname = 'fanstasma'
        form = EditOwnerNickname(initial={'nickname': proposed_nickname})

    context = {
        'form': form,
        'owner': owner,
    }

    return render(request, 'projects/owner_edit_nickname.html', context)

class OwnerCreate(CreateView):
    model = Owner
    fields = ['full_name', 'nickname']
    initial = {'nickname': 'fanstasma'}

class OwnerUpdate(UpdateView):
    model = Owner
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class ProjectCreate(CreateView):
    model = Project
    fields = ['name', 'owner', 'description', 'technologies', 'languages']
    initial = {'description': 'Project'}

class ProjectUpdate(UpdateView):
    model = Project
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('projects')
