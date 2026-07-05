from app.crud import (create_user , list_users, view_user, update_user, delete_user,
                       create_post, list_posts, view_post, update_post, delete_post, 
                       add_comment, view_comments, upodate_comment, delete_comment,
                       show_posts_by_user, show_comments_of_post, count_posts_written_by_every_user)


def user_management():
    while True:
        print("""===== BLOG MENU USER =====
    1. Create User
    2. List Users
    3. View User
    4. Update User
    5. Delete User
    6. Exit""")

        choice = input("Enter: ")
        match choice:
            case "6":
                break
            case "1":
                print("Creating a new User:")
                name = input("Enter name: ")
                email = input("Enter email: ")
                if create_user(name, email):
                    print(f"User {name} created successfully ")
                else:
                    print("User already exist")
            case "2":
                print("Listing All Users:")
                users = list_users()
                if users:
                    print("Users:")
                    print("-" * 75)
                    print(f"{'ID':<5} {'NAME'}")
                    print("-" * 75)
                    for user in users:
                        print(f"{user.id:<5} {user.name}")
                    print("-" * 75)
                else:
                    print("No users found")
            case "3":
                print("Viewing a user:")
                email = input("Enter user email: ")
                user = view_user(email)
                if user:
                    print(f"ID: {user.id}\nName: {user.name}\nEmail: {user.email}\nCreated at: {user.created_at}")
                else:
                    print("No user found")
            case "4":
                print("updating a user:")
                email = input("Enter user email: ")
                new_name = input("Enter new name: ")
                user = update_user(email, new_name)
                if user:
                    print("User name changed successfully")
                    print(f"New name: {user.name}")
                else:
                    print("Name change failed, email not found")
            case "5":
                print("deleting a user:")
                email = input("Enter user email: ")
                user = delete_user(email)
                if user:
                    print("User deleted successfully")
                else:
                    print("user deletion failed, email not found")
            case _:
                print("Please choose a right option")


def post_management():
    while True:
        print("""===== POST MENU =====

    1. Create Post
    2. List Posts
    3. View Post
    4. Update Post
    5. Delete Post
    6. Back""")

        choice = input("Enter: ")
        match choice:
            case "6":
                break
            case "1":
                print("Creating a new post:")
                try:
                    user_id = int(input("Enter user ID: "))
                except ValueError:
                    print("User ID must be a number.")
                    continue
                title = input("Enter post title: ")
                content = input("Post content: ")
                publish = input("Publish now? (1 = Yes, 2 = Draft): ")
                published = publish == "1"
                post = create_post(user_id, title, content, int(published))
                if post:
                    print("Post created successfully")
                    print(f"Post Owner: {post.user.name}\nPost ID: {post.id}\nPost title: {post.title}\nPost content: {post.content}\nPost published: {post.published}\nPost created at: {post.created_at}")
                else:
                    print("User does not exist")
            case "2":
                print("Listing all posts:")
                posts = list_posts()
                print("-" * 75)
                print(f"{'ID':<5} {'OWNER':<20} {'TITLE'}")
                print("-" * 75)
                for post in posts:
                    print(f"{post.id:<5} {post.user.name:<20} {post.title}")
                print("-" * 75)
            case "3":
                try:
                    post_id = int(input("Enter post ID: "))
                except ValueError:
                    print("Post ID must be a number.")
                    continue
                post = view_post(post_id)
                if post:
                    print(f"Post Owner: {post.user.name}\nPost ID: {post.id}\nPost title: {post.title}\nPost content: {post.content}\nPost published: {post.published}\nPost created at: {post.created_at}")
                else:
                    print("Post does not exist")
            case "4":
                try:
                    post_id = int(input("Enter post ID: "))
                except ValueError:
                    print("Post ID must be a number.")
                    continue
                    
                update = input("""What do you want to update?
1. Title
2. Content
3. Cancel\n""")
                if update == "1":
                    title = input("Enter new title: ")
                    post = update_post(post_id, new_title=title)
                elif update == "2": 
                    content = input("Enter new content: ")
                    post = update_post(post_id, new_content=content)
                else:
                    continue

                if post:
                    print(f"Post ID: {post.id}\nPost title: {post.title}\nPost content: {post.content}")
                else:
                    print("Post does not exist")
            case "5":
                try:
                    post_id = int(input("Enter post ID: "))
                except ValueError:
                    print("Post ID must be a number.")
                    continue
                post = delete_post(post_id)
                if post:
                    print("Post deleted successfully")
                else:
                    print("Post deletion failed, Post not found")
            case _:
                print("Please choose a right option")

def comment_managemnet():
    while True:
        print("""===== COMMENT MENU =====

    1. Add comment to a post
    2. View comments of a post
    3. Update comment
    4. Delete comment
    5. Back""")
        
        choice = input("Enter: ")
        match choice:
            case "5":
                break
            case "1":
                try:
                    user_id = int(input("Enter user ID: "))
                except ValueError:
                    print("User ID must be a number.")
                    continue              
                try:
                    post_id = int(input("Enter post ID: "))
                except ValueError:
                    print("Post ID must be a number.")
                    continue
                comment = input("Enter comment: ")

                commented = add_comment(user_id, post_id, comment)

                if commented:
                    print(f"Comment successfully added: {commented.content}")
                else:
                    print("Comment Failed")
            case "2":
                try:
                    post_id = int(input("Enter post ID: "))
                except ValueError:
                    print("Post ID must be a number.")
                    continue
                comments = view_comments(post_id)
                if comments:
                    for comment in comments:
                        print(f"Post:{comment.post.title}\nOwner: {comment.user.name}\nComment: { comment.content}\nComment ID: {comment.id}\n")
                else:
                    print("Post not found")
            case "3":
                try:
                    comment_id = int(input("Enter comment ID: "))
                except ValueError:
                    print("Comment ID must be a number.")
                    continue
                new_comment = input("Enter new comment: ")
                update = upodate_comment(comment_id, new_comment)
                if update:
                    print(f"Comment edited successfully: {update.content}")
                else:
                    print(" Comment does not exist")
            case "4":
                try:
                    comment_id = int(input("Enter comment ID: "))
                except ValueError:
                    print("Comment ID must be a number.")
                    continue
                comment = delete_comment(comment_id)
                if comment:
                    print("Comment deleted successfully")
                else:
                    print("Comment deletion failed, Comment not found")
            case _:
                print("Please choose a right option")


def special_functions():
    while True:
        print("""===== COMMENT MENU =====

    1. Show all posts by a user
    2. Show all comments for a post
    3. Count posts written by every user
    4. Delete comment
    5. Back""")
        
        choice = input("Enter: ")
        match choice:
            case "5":
                break
            case "1":
                try:
                    user_id = int(input("Enter user ID: "))
                except ValueError:
                    print("User ID must be a number.")
                    continue                 
                posts = show_posts_by_user(user_id)
                if posts:
                    print("-" * 75)
                    print(f"{'POST ID':<5} | {'POST TITLE'}")
                    print("-" * 75)
                    for post in posts:
                        print(f"{post.id:<5} | {post.title}")
                    print("-" * 75)
                else:
                    print("User does not exist")
            case "2":
                try:
                    post_id = int(input("Enter post ID: "))
                except ValueError:
                    print("Post ID must be a number.")
                    continue
                comments = show_comments_of_post(post_id)
                if comments:
                    print("-" * 75)
                    print(f"{'COMMENT ID':<5} {'COMMENT CONTENT':<25} {'COMMENT OWNER':<20} {'POST TITLE'}")
                    print("-" * 75)
                    for comment in comments:
                        print(f"{comment.id:<5} {comment.content:<25} {comment.user.name:<30} {comment.post.title}")
                    print("-" * 75)
                else:
                    print("Post not found")
            case "3":
                results = count_posts_written_by_every_user()

                print("-" * 35)
                print(f"{'USER':<20}{'POSTS'}")
                print("-" * 35)

                for name, count in results:
                    print(f"{name:<20}{count}")                             
                
                        


def run_menu():
    while True:
        print("""===== BLOG SYSTEM =====
    1. User Management
    2. Post Management
    3. Comment Management
    4. Special functions
    5. Exit""")
        
        management = input("Enter: ")
        match management:
            case "5":
                print("Program exited...")
                break
            case "1":
                user_management()
            case "2":
                post_management()
            case "3":
                comment_managemnet()
            case "4":
                special_functions()
            case _:
                print("Please choose a right option")




            


