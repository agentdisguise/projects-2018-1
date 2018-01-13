# The Server
from templating import render
from tornado.ncss import Server, ncssbook_log # ncssbook_log --> Optional | The logs will be more legible and easyer to follow / understand
from database.seeker import *
from database.position import Position
from database.position import get_position
from database.position import return_all_positions

#user = Seeker("James","Curran", "1/1/2012", "000", "james@ncss.com", "Sydney", ["Univeristy of Sydney - Bachelor of Science", "PhD in Computing Linguistics @ Sydeny Univeristy"], ["Coding","Running buisinesses","Reading storiess", "spelling"], ["Python", "everythgin"], ["NCSS"])

def index_handler (request):
    return render(request, 'index.html',{"login": check_logged_in(request)})

def profile_handler (request, user_id):
    '''
    if user_id == '1':
        with open('profile.html') as p:
            profile_html = p.read()
            profile_html = render(profile_html, {"user": user})
            request.write(profile_html)
    '''
    customer = get_seeker(user_id)
    if customer == None:
        render(request, "pagenotfound.html",{"login": check_logged_in(request)})
    else:
        render(request, "profile.html", {"user": customer, "login": check_logged_in(request)})



def profilelistpage_handler(request):
    seekers = get_seekers()
    render(request, 'profilelistpage.html', {"seekers": seekers, "login": check_logged_in(request)})

def searchresult_handler(request):
    request.write("Page Under Construction")

def about_handler(request):
    request.write("Page Under Construction")

def positionlist_handler(request):
    positionlist = return_all_positions()
    render(request, "positionlist.html", {"position": positionlist, "login": check_logged_in(request)})

def position_handler(request, page_id):
    position_information = get_position(page_id)
    render(request, "positioninformation.html", {'position': position_information, "login": check_logged_in(request)})

def map_handler(request):
    request.write("Page Under Construction")

def login_handler(request):
    render(request, "login.html", {"error": "", "login": check_logged_in(request)})

def post_login_handler(request):
    user = get_seeker_by_username(request.get_field('username'))
    if user:
        # check if password is correct
        if user.password == request.get_field('password'):
            request.set_secure_cookie('user_id', str(user.id))
            request.redirect("/")
        else:
            render(request, "login.html", {"error":"Incorrect password", "login": check_logged_in(request)})
    else:
        render(request, "login.html", {"error":"Incorrect username", "login": check_logged_in(request)})

def check_logged_in(request):
    user_id = request.get_secure_cookie('user_id')
    print(user_id)
    if user_id:
        return get_seeker(user_id.decode("UTF-8"))

def logout_handler(request):
    request.clear_cookie('user_id')
    request.redirect('/')

# Handler to display the form
def profile_creator_handler(request):
    render(request, 'createprofile.html',{"login": check_logged_in(request)})

# Handler for creating a new profile (for submiting the form, handle the returned post)
def finished_profile_handler(request):
    #add username later
    profile_fields = ['fname', 'lname', 'birthdate', 'phone', 'email', 'city', 'education', 'hobbies', 'skills', 'username', 'password', 'bio']
    field = []

    password = request.get_field('password')
    confpass = request.get_field('passwordconf')

    if password != confpass:
        request.redirect('/profilecreation/')

    for f in profile_fields:
        field.append(request.get_field(f))

    create_seeker(field)
    request.redirect('/')

def pagenotfound_handler(request):
    render(request, 'pagenotfound.html', {"login": check_logged_in(request)})


server = Server() # Create a server object
server.register(r'/', index_handler)
server.register(r'/about/', about_handler)
server.register(r'/profile/',profilelistpage_handler)
server.register(r'/searchresult/', searchresult_handler)
server.register(r'/position/', positionlist_handler)
server.register(r'/position/(\d+)/', position_handler) # Dynamic page | takes in a user id which is used
server.register(r'/profile/(\d+)/', profile_handler) # Dynamic page | takes in a user id which is used
server.register(r'/map/', map_handler)
server.register(r'/profilecreation/', profile_creator_handler, post = finished_profile_handler)
server.register(r'/login/', login_handler, post = post_login_handler)
server.register(r'/logout/', logout_handler)
server.register(r'/.*', pagenotfound_handler)
server.run() # Runs Server
