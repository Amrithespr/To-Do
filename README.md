## To-Do

# Setup

  Download the zip file and extract it to the Desktop.
  
  Open the terminal and enter the directory (Desktop/To-Do-main/To-Do-main/todoproject) where the manage.py file is present.

  Now install Python  (pip install python), and set up the environmental variables correctly.
  Install Django (pip install Django)

  open the project folder in any ide (eg. visual studio code)
  
  open views.py inside todoapp (Desktop/To-Do-main/To-Do-main/todoproject)

  # on scrolling down you can see, the following code

  //Save the markdown content locally
  
  file_name = f"{project.title}.md"
  
  file_path = os.path.join("ENTER PATH OF FOLDER", file_name)  # Specify the directory where you want to save the markdown file

  # change ENTER PATH OF FOLDER , with the directory where you want to save the markdown file in your local system

  # just below that you can see,

  //Create a secret gist using GitHub API
  
  github_token = "YOUR GITHUB PERSONAL ACCESS TOKEN"  #  Replace with your github personal access token
   
  # change YOUR GITHUB PERSONAL ACCESS TOKEN , with  your GitHub personal access token. 
  
  # GitHub personal access token can be accessed by
  go to github settings, go to developer settings, go to personal access tokens, click on Tokens (classic),
  click on generate new token, select generate new token (classic)

  then, add a note,  allow check mark on public_repo and gist  options only. Then click generate token.
  Make sure to copy your personal access token now. You won’t be able to see it again!
  

# How to Run the project

  Enter the following command in the terminal after correctly specifying the project directory (Desktop/To-Do-main/To-Do-main/todoproject).
    python manage.py runserver

   http://127.0.0.1:8000/   Enter this link in a browser

   Now the web application opens with a Registration Form,
   After successful registration and Login, you will be redirected to the home page

   On the home page, you can create as many Projects as you want.

   To view a particular Project and to add and manage todos, you may click the " View Tasks " button

   On entering a particular project, you can add as many tasks as you want, with functionalities of add, update, and delete options.

   To mark a todo as pending or completed you can use the "update" button.

   After the successful creation of tasks, you can return to the home page to export the summary as a secret gist.

   On clicking the "Export summary as gist" button, it will export the summary as a secret gist and save the 
   exported gist file to the local system (as markdown)

   Before that make sure you have successfully completed the setup instructions

# How to Test the project
  go to the directory (Desktop/To-Do-main/To-Do-main/todoproject) where manage.py file is present

  run the command   python manage.py test    in the terminal to get the test results 
  
  
