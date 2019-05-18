import pyrebase
import os

#Connection to firebase database:
config={
	'apiKey': 'AIzaSyBnT_yLcosqucPXBEHcS4Tz2C1oD3K2200',
    'authDomain': 'getlocation-1552472926020.firebaseapp.com',
    'databaseURL': 'https://getlocation-1552472926020.firebaseio.com',
    'projectId': 'getlocation-1552472926020',
    'storageBucket': 'getlocation-1552472926020.appspot.com',
    'messagingSenderId': '517749307018'
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()

#for removing user from database by admin
class Remove_User:
	def remove_user(self, poll_id, group,user):
		print(poll_id)
		db.child("polls-data").child("group").child(group).child("members/"+poll_id).remove()
		db.child("users/"+user).remove()
		return 'Done'

#for removing polls from db by admin
class Remove_Poll:
	def remove_poll(self, poll_id, group):
		print(poll_id)
		db.child("polls-data").child("group").child(group +'/'+ poll_id).remove()
		return 'Done'

#for adding polls to firebase database
class Add_Poll:
	def add_poll(self, poll_data, group):
		db.child('polls-data').child('group').child(group).push(poll_data)
		return 'Done'

class Get_Polls:
	def get_poll_by_group(self, group):
		get_polls=db.child('polls-data').child('group').child(group).get()
		return get_polls.val()

#for registering new users and admin
class SignUp:
	def signup_user(self, email, password, user_name, user_group):
		user = auth.create_user_with_email_and_password(email, password)
		data = {'email': email,'group':user_group}
		member = {'user_name' : user_name}
		results = db.child('users').child(user_name).set(data, user['idToken'])
		db.child('polls-data').child('group').child(user_group).child('members').push(member)

class SignIn:
    def signin_user(self, email, password):
        user = auth.sign_in_with_email_and_password(email, password)
        return user


class Poll_Vote:
	def submit_vote(self, choice_no, poll_id,group,user_name):
		get_choice=db.child('polls-data').child('group').child(group).child(poll_id).child('choices').get()
		current_votes=get_choice.val()[int(choice_no)]['votes']
		updated_votes=current_votes+1
		user_polls=db.child('users').child(user_name).child('prev-polls').push({'id':poll_id})
		res=db.child('polls-data').child('group').child(group).child(poll_id).child('choices').child(choice_no).child('votes').set(updated_votes)
		return res

class Prev_Polls:
	def get_previous_polls(self, user_name):
		user_polls_array=[]
		user_polls=db.child('users').child(user_name).child('prev-polls').get()
		user_polls=user_polls.val()
		try:
			user_polls_array=[user_polls[poll]['id'] for poll in user_polls]
			return user_polls_array
		except:
			return []

class Get_Members:
	def get_group_members(self, user_name, group):
		get_members=db.child('polls-data').child('group').child(group).child('members').get()
		group_members=get_members.val()
		res = {}
		for a in group_members:
			res[group_members[a]['user_name']]=a
		print(res)
		#res=[group_members[a]['user_name'] for a in group_members]
		#id = [a for a in group_members]
		return res