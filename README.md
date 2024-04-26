How to run this code, run following commands:

pip install django	

pip list

pip3 install djangorestframework-simplejwt

python manage.py runserver (This lets you access your project with a web browser at the local address)

### Project goals: 
The goal of this project is to provide drug users with a secure way to log their drug intake and monitor their substance abuse habits. By implementing a digital tracking system, we aim to empower individuals struggling with addiction to take control of their habits and make informed decisions about their health. The idea is based on the principle of "if you can measure it, you can manage it." Through this platform, users can record their drug consumption patterns, track their progress toward recovery, and gain insights into the impact of their substance abuse on their overall well-being.

### Significance of the project: 
Substance abuse and addiction pose significant challenges to individuals, families, and communities worldwide. Addiction is a complex and multifaceted problem that affects people from all walks of life, leading to devastating consequences such as health problems, social isolation, financial instability, and legal issues. By providing a tool for individuals to monitor their drug intake, our project addresses a critical need in the realm of addiction recovery and harm reduction. The significance of this project lies in its potential to support individuals in overcoming addiction, promoting healthier behaviors, and ultimately improving their quality of life.
Recognizing your addiction and showing the willingness to manage it is the first and the most crucial step to overcoming substance abuse. Our platform is meant to be used by individuals who have reached that step and are ready to take action to overcome their addiction. 

### Installation and usage instructions: 
To install and use the software, follow these steps:

1. Clone the GitHub repository to your local machine.
2. Install the necessary dependencies by running 
   `pip install django`
   `pip3 install djangorestframework-simplejwt`

3. Navigate to project directory and set up the database by running `python manage.py migrate`.
4. Start the development server with `python manage.py runserver`.
5. Access the application through your web browser at `http://localhost:8000`.
6. Click register to make a new account 
7. On the login page, enter your username and password to log in
8. Click the Add Drug Intake button to log alcohol and nicotine usage
9. For alcohol, select the kind of drink from the dropdown, enter the number of drinks consumed, and click the Add Alcohol Intake button 
10. For cigarettes, enter the number of cigarettes consumed and click the Add Cigarette Intake button 
11. When done adding, navigate to the dashboard using the Dashboard link in the nav bar to view your drug intake log. 

### Code structure: 
The code follows a modular structure, with separate files for models, views, forms, and templates. 
The model.py file contains the database schemas for the User, Alcohol Intake, and Cigarette Intake. The two intake models are associated with a user, hence they use the user as a foreign key in their tables. 

The urls.py file contains the URL routing for when a user makes an HTTP request to a specific URL and maps the URL to a particular function in views.py

The views.py file contains the business logic of the program. Based on the endpoint from which it receives the HTTP request, the corresponding function to handle that request is called. Here, views.py contains the logic to sign up a user and send their data to the User model to be stored. For login, it retrieves data from the user model to verify the credentials. For the dashboard, views display the data from the user model and the two intake models. This is also where the logic to calculate the toxins is and where the thread to calculate the BAC is created and started and the database is updated with the updated BAC value. Views also render the HTML templates.

The forms.py file holds the different forms used in the program such as signup, login, and alcohol and cigarette intake forms. They are passed on to the HTML files through the views.py file.  

![Untitled Diagram drawio](https://github.com/Taazkir/Toxin-Logger-for-Drug-Abuse/assets/107087417/c11ce19e-1c4b-4e83-9b2f-6f2e7a08e6fe)


### List of functionalities:
The application allows users to:
- Data privacy through secure login
- Log their alcohol and cigarette intake.
- Calculate BAC levels based on user input.
- Continually update BAC levels with the passage of time using threads
- Display BAC, toxin levels, and other relevant information on the user dashboard.
- Storing all relevant data in a database
- Provide admin-level privileges to manage the database
- Provide a user-friendly interface for easy interaction.

### Test Results: 

<img width="997" alt="Screenshot 2024-04-26 at 2 00 36 PM" src="https://github.com/Taazkir/Toxin-Logger-for-Drug-Abuse/assets/107087417/47068b7f-88bb-43d6-aff5-0459b5b1bef1">

Signup-Login and saving to database

<img width="1130" alt="Screenshot 2024-04-26 at 2 03 29 PM" src="https://github.com/Taazkir/Toxin-Logger-for-Drug-Abuse/assets/107087417/30855343-4c08-4320-be25-6d9e0093aebc">

<img width="1204" alt="Screenshot 2024-04-26 at 2 05 56 PM" src="https://github.com/Taazkir/Toxin-Logger-for-Drug-Abuse/assets/107087417/5de5c0cb-b2f0-4fa6-aaa4-c78417beed6b">

Retrieve user info from database and display to dashboard

<img width="1204" alt="Screenshot 2024-04-26 at 2 06 15 PM" src="https://github.com/Taazkir/Toxin-Logger-for-Drug-Abuse/assets/107087417/6fef0720-6fa4-4103-865c-1a17444eebd4">

Adding intake data and updating database and dashboard

<img width="1204" alt="Screenshot 2024-04-26 at 2 06 49 PM" src="https://github.com/Taazkir/Toxin-Logger-for-Drug-Abuse/assets/107087417/80b28387-b474-4a40-8f9f-a6f8990624c8">

<img width="1204" alt="Screenshot 2024-04-26 at 2 07 05 PM" src="https://github.com/Taazkir/Toxin-Logger-for-Drug-Abuse/assets/107087417/cb39f79b-8231-4de1-882a-c7e0e5cd507e">

<img width="2029" alt="Screenshot 2024-04-26 at 2 08 15 PM" src="https://github.com/Taazkir/Toxin-Logger-for-Drug-Abuse/assets/107087417/92291b6d-9fc8-41cb-9862-f8d4ec633378">


### Discussion and Conclusion:
In developing this project, we applied key learnings in the areas of concurrency, security, and system design. The utilization of threads played a crucial role in the implementation of real-time updates for Blood Alcohol Concentration (BAC) levels, demonstrating our understanding of concurrent programming concepts.

The threading mechanism allowed us to create a separate thread responsible for continuously updating BAC levels for users based on their alcohol intake. By employing threads, we were able to simulate the passage of time and the decrease of BAC levels over a specified interval. This practical application of threading showcases our comprehension of how to manage concurrent tasks effectively within a software system.

Furthermore, the integration of secure login functionality underscores our knowledge of security principles in software development. We implemented authentication mechanisms to ensure that only authorized users can access the application and log their drug intake data. By incorporating secure login features, we demonstrate our commitment to safeguarding user privacy and protecting sensitive information.

Overall, the project successfully achieves its objectives of providing a secure and user-friendly platform for tracking drug intake. However, there are some limitations and challenges that need to be addressed, such as the accuracy of the levels of toxins and BAC calculations, implementing additional features for comprehensive substance abuse monitoring, such as tracking mood changes, and providing resources for addiction recovery. Moving forward, we recognize the importance of continuous improvement and refinement of the application to address emerging challenges and meet the evolving needs of users in the fight against substance abuse and addiction.
