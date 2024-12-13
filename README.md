# **Password Manager Application for COM5013 Algorithms and Data Structures**

This is my password manager application using Tkinter, python for the COM5013 assignment. It implements the usage of the AES encryption/decryption cryptography algorithm on passwords for the login process of the application. It also implements search and sort algorithms on searching database table records by retrieving user queries or sorting by certain fields. I implemented linear search and binary search (specifically iterative instead of recursive) for the search algorithms. For the sort algorithms, I implemented merge sort, bubble sort and quick sort.

---

## **Functionality**

- The homepage has two buttons: signup or login. Pressing either will lead you to their respective pages, with tabs at the top to switch between them for accessibility.
- Signing up prompts user to enter details. Certain constraints, such as all fields being required or password and confirm passwords must be the same, will make sure the user enters the right details.
- Succeeding in doing so takes them to the login page. An AES algorithm function is applied to the password, which will save the salt, initialisation vector and the encrypted password to the users database table.
- The login page is similar to signing up, but must enter the correct details. The program decrypts the password and matches it to what the user entered if it is correct.
- If correct, the password manager window opens, showing a treeview of all the records of the passwords that the user has saved.
- User is able to add, edit or delete records in the passwords database table.
- The search bar on the window dynamically searches all fields for what matches the user's query, and refreshes the treeview to show accordingly.
- The button next to the search bar opens the advanced search window. The user may enter a query, and then tick ONLY the fields that they wish to search the query against. When pressing submit, the treeview refreshes and displays what the user searched for.
- The button besides the advanced search window refreshes the treeview. I added this because the binary search algorithm may not show the right records, as I occasionally forgot to sort the unordered records,
- Sort by: is a dropdown box that has all the visible fields of the database table. by clicking on one of the fields, the records are sorted and refresh the treeview to show the sorted records.
- The options button allows the user to choose which algorithms they would like to use for the advanced search window and the sort by dropdown box. For example, user may want to change the setting to use binary search and use bubble sort, and may change it by selecting those options and saving the settings.

- Tested functionality by adding 1000 mock value records in for the two current users in database. To test, see below.
- This application has no way of logging out the user. It is also unable to save settings for all sessions, e.g. wanting to make binary search the default algorithm.
- I wanted to add more sort algorithms, such as radix sort or insertion sort, but struggled to implement binary search and quick sort. Unable to do so in time constraints.

---

## **Testing and Issues**

- To test, there were two users that had separate user ids. This is what the password records link to, and users are only shown passwords that match their unique user id. These two users were added for testing purposes only and had mock records linked to them.
- To see how different they are, the two usernames and passwords are as follows:

USER_ID = 1
Username: JazielNarag 
Password: Password123

USER_ID = 2
Username: TestUsername
Password: Testing123

- I forgot that I needed a github repository and will be deducted marks. In an attempt to salvage that issue, I put all my saved past revisions of my code where I had issues, by putting them in my past commits.
- Most issues I ran into were implementing the algorithms and figuring out what parameters I needed to call. I also had many mutual top-level imports which python thought I had tried to call third-party modules. Another issue is that I kept using global variables, which in itself is bad practice, so I tried to cut down to one global variable overall.

- Connection details are as follows for MySQL:

username: login_test
password: LoginTest123
host: 127.0.0.1
port: 3306
connection name: LogInConnection
