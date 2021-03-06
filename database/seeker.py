import sqlite3
import hashlib

class Experience(object):
    def __init__(self, companyname, experiencetype, rating, person_id):
        self.id = None
        self.companyname = companyname
        self.experiencetype = experiencetype
        self.rating = rating
        self.person_id = person_id

    def save(db_file, self):
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("""INSERT INTO experience (companyname, experiencetype, rating, person_id)
        VALUES (?, ?, ?, ?)""", (self.companyname, self.experiencetype, self.rating, self.person_id))
        self.id = cur.lastrowid
        conn.commit()
        cur.close()
        conn.close()


class Seeker(object):
    """Person searching for work experience."""
    def __init__(self, fname, lname, birthdate, phone, email, city, education, hobbies, skills, username, password, bio, id = None):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.birth_date = birthdate
        self.phone = phone
        self.email = email
        self.city = city
        self.education = education
        self.hobbies = hobbies
        self.skills = skills
        self.experiences = []
        self.username = username
        self.password = password
        self.bio = bio
    def __str__(self):

        return "fname: '{}', lname: '{}', birthdate: '{}', phone: '{}', email: '{}', city: '{}', eductaion: '{}', hobbies: '{}', skills: '{}', id: '{}', experiences: '{}', username: '{}', password: '{}', bio: '{}'".format(self.fname, self.lname, self.birth_date, self.phone, self.email, self.city, self.education, self.hobbies, self.skills, self.id, self.experiences, self.username, self.password, self.bio)

    def add_experience(self, companyname, experiencetype, rating):

        exp = Experience(companyname, experiencetype, rating, self.id)
        exp.save()
        self.experiences.append(exp.id)

    def gravatar(self):
        h = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon'.format(h)


#Find the seeker with specific id and return information
def get_seeker(db_file, id):
    """Returns information about a seeker from the database."""
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM seekers_personal WHERE id = ?;",(id,))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if row == None:
        return None
    id, fname, lname, birth_date, phone, email, city, education, hobbies, skills, username, password, bio = row
    user = Seeker(fname, lname, birth_date, phone, email, city, education, hobbies, skills, username, password, bio, id)
    return user



def create_seeker(db_file, info):
    """Creates a new seeker."""
    fname, lname, birth_date, phone, email, city, education, hobbies, skills, username, password, bio = info
    user = Seeker(fname, lname, birth_date, phone, email, city, education, hobbies, skills, username, password, bio)
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    #print("""INSERT INTO seekers_personal (id, fname, lname, birth_date, phone, email, city, education, hobbies, skills, experiences)
    #            VALUES ('?','?','?','?','?','?','?','?','?','?','?')""".format(self.id, self.fname, self.lname, self.birth_date, self.phone, self.email, self.city, self.education, self.hobbies, self.skills, self.experiences))
    cur.execute("""INSERT INTO seekers_personal (fname, lname, birth_date, phone, email, city, education, hobbies, skills, username, password, bio)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?);""",(fname, lname, birth_date, phone, email, city, education, hobbies, skills, username, password, bio))
    user.id = cur.lastrowid
    conn.commit()
    cur.close()
    conn.close()
    return user

def get_experience(db_file, id):
    """Returns information about an experience from the database."""
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM experience WHERE id = ?;",(id,))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    id, companyname, experiencetype, rating, person_id = row
    experience = Experience(companyname, experiencetype, rating, person_id)
    return experience

def get_seekers(db_file):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM seekers_personal;")

    info = []
    for row in cur:

        id, fname, lname, birth_date, phone, email, city, education, hobbies, skills, username, password, bio = row
        user = Seeker(fname, lname, birth_date, phone, email, city, education, hobbies, skills, username, password, bio, id)
        info.append(user)

    conn.commit()
    cur.close()
    conn.close()

    return info

def get_seeker_by_username(db_file, username):
    """Returns information about a seeker from the database."""
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM seekers_personal WHERE username = ?;",(username,))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if row == None:
        return None
    id, fname, lname, birth_date, phone, email, city, education, hobbies, skills, username, password, bio = row
    user = Seeker(fname, lname, birth_date, phone, email, city, education, hobbies, skills, username, password, bio, id)
    return user

#cur.close()
#conn.close()
#create DB call in sepereate files (create databse file)
# class function to create user (INSERT INTO etc.)
# class function to get user from db
