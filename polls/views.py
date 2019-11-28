from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Choice, Question
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django import forms
from bootstrap_datepicker_plus import DateTimePickerInput


@method_decorator(login_required, name='dispatch')
# Generic Class-Based Views (GCBV)
class QuestionListView(ListView):
    model               = Question
    template_name       = 'polls/question_list.html'
    context_object_name = 'questions'
    paginate_by         = 50
    ordering            = ['id'] # if -id Descending id then Ascending
    def get_context_data(self, **kwargs):
        context   = super(QuestionListView, self).get_context_data(**kwargs)
        question  = self.get_queryset()
        page      = self.request.GET.get('page')
        paginator = Paginator(question, self.paginate_by)
        try:
            question = paginator.page(page)
        except PageNotAnInteger:
            question = paginator.page(1)
        except EmptyPage:
            question = paginator.page(paginator.num_pages)
        context['question'] = question
        return context

class NewPostView(CreateView):
    model         = Question
    fields        = ['question_text', 'pub_date']
    template_name = 'polls/question_form.html'
    success_url   = reverse_lazy('polls:list')
    def get_form(self, form_class=None):
        form = super(NewPostView, self).get_form(form_class)
        form.fields['pub_date'].initial = timezone.now()
        return form

class EditView(UpdateView):
    model               = Question
    fields              = ['id','question_text','pub_date']
    template_name       = 'polls/edit_form.html'
    context_object_name = 'question'
    def get_success_url(self):
        return reverse_lazy('polls:list')

class RemoveView(DeleteView):
    model         = Question
    template_name = 'polls/post_confirm_delete.html'
    success_url   = reverse_lazy('polls:list')

# Class-Based View (CBV)
class IndexView(generic.ListView):
    template_name       = 'polls/index.html'
    # for data list store in this var check in 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        # return Question.objects.order_by('-pub_date')[:5] # returns only five as per pub_date
        return Question.objects.all()

class DetailView(generic.DetailView):
    model         = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model         = Question
    template_name = 'polls/results.html'

# Function-Based View (FBV)
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

class AddChoices(CreateView):
    model = Choice
    fields = ['id','choice_text']
    template_name = 'polls/choice_form.html'
    def form_valid(self, form):
        form.instance.question_id = self.kwargs['question_id']
        return super(AddChoices, self).form_valid(form)
    def get_success_url(self):
        question_id = self.kwargs['question_id']
        success_url = reverse_lazy('polls:vote', kwargs={'question_id': question_id})
        return success_url

class AboutView(generic.ListView):
    model         = Question
    template_name = 'polls/about.html'

class ContactView(generic.ListView):
    model         = Question
    template_name = 'polls/contact.html'
