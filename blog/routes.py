from blog.forms import Registrationform,Loginform,AccountForm,CreatePost
from blog.models import User,Post
from blog import app,bcrypt,db
from flask import render_template,url_for,flash,redirect,request,abort
from flask_login import login_user,current_user,logout_user,login_required
import os
import secrets
from PIL import Image 



@app.route("/home")
@app.route("/")
def home():
	page=request.args.get('page',1,type=int)


	post=Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=2)
	return render_template('home.html',post=post,name='Home')

@app.route("/about")
def about():
	return render_template('about.html',name='About')

@app.route("/register",methods=['GET','POST','PUT','DELETE'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form=Registrationform()
	if form.validate_on_submit():
		hash_pass=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		check=User.query.filter_by(username=form.username.data).first()
		check1=User.query.filter_by(email=form.email.data).first()
		if(check==None and check1==None):
			user=User(username=form.username.data,email=form.email.data,password=hash_pass)
			db.session.add(user)
			db.session.commit()
			flash(f'Account created for ' + form.username.data ,'success')
			return redirect(url_for('login'))
		else:
			if(check1!=None):
				flash(f'Account already existed for ' + form.email.data ,'danger')
			if(check!=None):
				flash(f'Account already existed for ' + form.username.data ,'danger')

			return redirect(url_for('register'))

	return render_template('register.html',name='Register',form=form)
@app.route("/login",methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form=Loginform()
	if form.validate_on_submit():

		val=User.query.filter_by(email=form.email.data).first()
		if(val!=None):
			password=val.password
			# user_password_entered=form.password.data
			if(bcrypt.check_password_hash(password,form.password.data)):	
				# flash(f'Logged in successfully','success')
				login_user(val)
				next_page=request.args.get('next')
				return redirect(next_page) if next_page else redirect(url_for('home'))
			else:
				flash(f'incorrect password','danger')
				return redirect(url_for('login'))
	return render_template('login.html',name='Login',form=form)


@app.route("/logout",methods=['GET','POST'])
def logout():
	logout_user()
	return redirect(url_for('home'))
 
def save_pict(form_pict):
	random_hex=secrets.token_hex(8)
	_,f_ext=os.path.splitext(form_pict.filename)
	picture_fn=random_hex+f_ext
	path=os.path.join(app.root_path,'static/profile_pics',picture_fn)
	output=(125,125)
	i=Image.open(form_pict)
	i.thumbnail(output)
	print(path)
	i.save(path)
	return picture_fn

@app.route("/account",methods=['GET','POST'])
@login_required
def account():
	form=AccountForm()
	form.email.data=current_user.email
	form.username.data=current_user.username
	
	print(current_user.email)
	if form.validate_on_submit():
		if form.picture.data:
			pict_file=save_pict(form.picture.data)
			# print(pict_file)
			# pict=pict_file[-21:]
			current_user.profile=pict_file

		current_user.username=form.username.data
		current_user.email=form.email.data
		db.session.commit()
		flash(f'Account Updated','success')
		return redirect(url_for('account'))








	image=url_for('static',filename='profile_pics/'+current_user.profile)
	#print(image)
	return render_template('account.html',name='Account',image=image,form=form)

@app.route("/post/new",methods=['GET','POST'])
@login_required
def new_post():
	form=CreatePost()

	if form.validate_on_submit():
		post=Post(title=form.Title.data,content=form.Content.data,author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('post created successfully','success')
		return redirect(url_for('home'))

	return render_template('create_post.html',name='New Post',form=form,legend=' New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
	post=Post.query.get_or_404(post_id)
	return render_template('post.html',name='POST',post=post)


@app.route("/post/<int:post_id>/update",methods=['GET','POST'])
@login_required
def update_post(post_id):
	post=Post.query.get_or_404(post_id)
	if post.author!=current_user:
		# flash('You are not allowed to edit this post','danger')
		abort(403)
	form=CreatePost()
	if form.validate_on_submit():
		post.title=form.Title.data
		post.content=form.Content.data
		db.session.commit()
		flash('Post Updated Successfully','success')
		return redirect(url_for('post',post_id=post.id))
	if request.method=='GET':
		print("heyeyeheyey")
		form.Title.default=post.title
		form.Content.default=post.content
		print("fool")
	return render_template('create_post.html',legend='Update Post',form=CreatePost(),name='Update Post')


@app.route("/post/<int:post_id>/delete",methods=['GET','POST'])
@login_required
def delete_post(post_id):
	post=Post.query.get_or_404(post_id)
	if post.author!=current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Post is Deleted','success')
	return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_post(username):
	page=request.args.get('page',1,type=int)
	user=User.query.filter_by(username=username).first_or_404()


	post=Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page,per_page=2)
	return render_template('user_post.html',post=post,name='Posts',user=user)

