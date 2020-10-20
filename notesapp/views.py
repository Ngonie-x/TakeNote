from django.shortcuts import render, redirect, reverse
from .models import Note, Categories
from .forms import NoteForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.generic import DeleteView, UpdateView


# Create your views here.

@login_required
def notes_list_index(request):
    try:
        # initialize notes and categorie
        notes = Note.objects.filter(user=request.user)
        categories = Categories.objects.filter(user=request.user)
    except Exception:
        print(e)
        pass
    
    if request.method == 'POST':
        # initialize notes form
        note_form = NoteForm(request.POST)

        # if the post is search
        if "searchbtn" in request.POST:
            search_word = request.POST['search']
            if search_word != '':
                try:
                    notes = Note.objects.filter(Q(user=request.user), Q(category__category__icontains=search_word) | Q(title__icontains=search_word) | Q(text__icontains=search_word))
                    categories = Categories.objects.filter(user=request.user)
                    return reverse('notesapp:list_index', args=(notes, categories, note_form))# if i remove the args it won't do anything, but if it's there it works but prints an error.
                except Exception as e:
                    # print(e)
                    pass

        else:
            
            # if the post is from the note_form
            if note_form.is_valid():
                new_note = note_form.save(commit=False)

                # get the user
                new_note.user = request.user

                # get the category
                try:
                    category = request.POST["category_select"]
                    obj_category = Categories.objects.get(user=request.user, category=category)
                    new_note.category = obj_category
                
                except:
                    category = request.POST["create-category"]
                    if category == '':
                        new_note.category, created = Categories.objects.get_or_create(user=request.user, category='General')
                    else:
                        obj_category = Categories.objects.create(user=request.user, category=category)
                        new_note.category = obj_category

                # save
                new_note.save()

                messages.success(request, "Your note has been saved.")

                return redirect('notesapp:list_index')

    else:
        note_form = NoteForm()

    return render(request, 'notesapp/list_index.html', {'notes':notes, 'categories':categories, 'note_form':note_form})


class NoteDeleteView(DeleteView):
    model = Note
    success_url = "/notes/"


@login_required
def update_note(request, pk):
    note = Note.objects.get(user=request.user, id=pk)
    categories = Categories.objects.filter(user=request.user)

    if request.method == 'POST':
       title = request.POST['title']

       category = request.POST['category_select']
       obj_category = Categories.objects.get(user=request.user, category=category)

       text = request.POST['text']

       note.title = title
       note.category = obj_category
       note.text = text

       note.save()

       messages.success(request, "Your note has been updated.")
       
       return redirect('notesapp:list_index')
    
    return render(request, 'notesapp/note_form.html', {'note':note, 'categories':categories})