from django.shortcuts import redirect

def with_team_created(view):
    def wrapper(request, *args, **kwargs):
        if not request.session.has_key('teamId'):
            print("with_team_created. Request without team created")
            return redirect('index')
        return view(request, *args, **kwargs)
    return wrapper

def without_team_created(view):
    def wrapper(request, *args, **kwargs):
        if request.session.has_key('teamId'):
            print("without_team_created. Request with team created")
            return redirect('questions')
        return view(request, *args, **kwargs)
    return wrapper