# Monthly Budgeting Planner
---

### Video Demo: URL will go here once recorded
---
### Description of webapp:

This webapp will allow users to record all of their monthly income, expenses and savings.

When users are first arriving to the page via route "/" they will be greeted with options to register or sign in. Once the user has registered they will be taken to the dashboard that will explain that there is currently a lack of information to present and then suggest to the user that they fill out at least the income and expenses forms to be able to see some visual data. 

All pages are linked within the apps navbar located at the top of the page. 

When the user visits the outgoings page, they are presented with a table of standard expenses to get them going, which they are able to edit as they see fit. This also applies to the income and saving forms. On the right hand side of every entry there is an trash icon that when clicked, the row will be deleted. At the bottom of each form there is an option to add another row to the table for custom entries. Once the user has completed filling out the form, they will click the submit button. The app will then check the form to make sure that each cell is filled out accordingly. 

Once the user has filled out the income and outgoings forms, the dashboard will then present totals for the each area and also a graph for outgoings, savings and a remaining cash balance. 

## SQLite

The project consists of a database named budget and 4 tables within.

Below is a schema of the database:

| Tables_in_budget |
------------------
| expenses         |
| income           |
| savings          |
| users            |

### Users Table

| Field      | Type         | Null | Key | Default | Extra          |
|---|---|---|---|---|---
| id         | int          | NO   | PRI | NULL    | auto_increment |
| username   | varchar(100) | NO   | UNI | NULL    |                |
| password   | varchar(200) | NO   |     | NULL    |                |
| data_added | datetime     | NO   |     | NULL    |                |

### Income table


| Field   | Type         | Null | Key | Default | Extra          |
|---|---|---|---|---|---
| id      | int          | NO   | PRI | NULL    | auto_increment |
| user_id | int          | NO   | MUL | NULL    |                |
| income  | varchar(100) | NO   |     | NULL    |                |
| amount  | float        | NO   |     | NULL    |                |

### Savings table


| Field   | Type         | Null | Key | Default | Extra          |
|---|---|---|---|---|---
| id      | int          | NO   | PRI | NULL    | auto_increment |
| user_id | int          | NO   | MUL | NULL    |                |
| income  | varchar(100) | NO   |     | NULL    |                |
| amount  | float        | NO   |     | NULL    |                |

### Expenses table


| Field   | Type         | Null | Key | Default | Extra          |
|---|---|---|---|---|---
| id      | int          | NO   | PRI | NULL    | auto_increment |
| user_id | int          | NO   | MUL | NULL    |                |
| expense | varchar(100) | NO   |     | NULL    |                |
| amount  | float        | NO   |     | NULL    |                |

## app.py

As with all flask apps, the main heart of the site is written in app.py.

We start by creating the database models for Users, Expenses, Income and Savings.

Within the dashboard function, python is calulating the total values that the user has inputted into each of the forms and then returning it via render_template where it will then be displayed to the user in both total values and a graph visual.

In the income function, there we have a list of possible incomes that the user can use as a base to fill out and edit as needed. The user is free to also delete what isnt needed and add more that are not on the list. This is also the same for outgoings and savings.

Once the user submits the form, the code is checking for any previous entries made by the user. If there query returns values, they are deleted and the database is updated with the most recent form. Again this process is the same for outgoings and savings. 

If the user is a returning user who has already filled out the form prior, the values will be returned to the user for viewing and editing. 

I have also added a login required decorator to many of the functions to make sure that they cannot be viewed by users who are not currently logged in. This has been applied to:
- dashboard
- income
- outgoings
- savings
- logout

## froms.py

For the user log in and registration, i have used the What The Forms package from flask. The forms could have been done with HTML and Python but the only reason I have used WTForms is to get more familiar with Flask and to get a wider knowledge on how forms can be created. 

## dashboard.html
The dashboard is what users will see when they login and register first. When the user firsts registers or has not yet filled out any of the forms, they will be shown a message explaining that they have not done so and are presented with links to expenses pages. 

Once the users has filled out at least provided data on their income and outgoings then they are presented with total figures of what they have coming in and going out based on the data that they have provided. There is also a chart that will allow users to visually see how much they are savings, spending on expenses and a remaining cash balance.

## income.html, outgoings.html, savings.html
As mentioned above, when users visit these pages for the first time, they are presented with an example list that they are free to edit as they see fit. Once the user clicks submit, they will be redirected to the dashboard which has been updated. If the users goes back to the form that they have already completed, they will see all their submitted data which can also be edited. 

## flash.html
In this project I have used flask flash messages to greet the user when logging in, logging out or registering, making any changes to their data and also for if their log in requirements are not correct.

## scripts.js
Javascript has enabled me to let user edit the tables that they wish to submit. By creating variables that contain HTML and simply insert a new row or delete a row within in the table with the click of a button. 

Also, using Chart.JS i have been able to produce a visual representation of their expenses in the form of a doughnut chart so users can see what 'slices' of the chart are being spent where and how much cash will be remaining. Also as the numbers that the chart is pulling contains commas, JavaScript has allowed me to edit the figures and remove the commas before being inserted to the graph.


## requirements.txt

For anyone who would like to download and make their own version of this monthly budget planner, i have included a list of requirements that the user would need to install for the app to run.