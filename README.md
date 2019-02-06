# NTU Student Union IT Entry Task

## Description
This project is a mini blog. Users who have registered on the blog can like and comment posts,
while admins can create, edit, delete posts; as well as register users to the blog.

This project is built on Django.

## How to use
Clone this repository, and type 

```python manage.py runserver```

on your terminal.

You should then be able to view the blog on `localhost:8000/blogs/`.

## Things to do

### User page
- Maintain on the same page after commenting on a post or login/logout
- Enable view comments without logging in
- Count only unhidden comments on index page
- `@login_required` for user page 
- No refresh after a like on a post
- Customize avatar for each user

### Admin page
- Dismissable success action message
- Modal 'yes/no' for post deletion
- Success action message for post deletion