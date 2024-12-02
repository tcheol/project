import mysql.connector
from datetime import date, timedelta

#mydb = mysql.connector.connect(
  #host="127.0.0.1",
  #user="root",
  #password="Tandon2024",
  #database = "librarydb"
#)

#mycursor = mydb.cursor()

#mycursor.execute("CREATE TABLE books (Bookid INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), author VARCHAR(255), genre VARCHAR(100), PublicationYear INT, AvaiableCopies INT DEFAULT 0)")
#mycursor.execute("CREATE TABLE members (MemberID INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), phoneNumber VARCHAR(20), membershipStartDate DATE, membershipEndDate DATE)")
#mycursor.execute("CREATE TABLE borrowedBooks (BorrowID INT AUTO_INCREMENT PRIMARY KEY, BookID INT, MemberID INT, BorrowDate DATE, ReturnDate DATE, IsReturned BOOLEAN DEFAULT FALSE)")
#mycursor.execute("CREATE TABLE transaction (TransactionID INT AUTO_INCREMENT PRIMARY KEY, BorrowID INT, TransactionDate DATE, Transaction ENUM('Borrow','Return')")


#mycursor.execute("SHOW TABLES")

#for x in mycursor:
    #print(x)

def connect_to_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Tandon2024",
        database = "librarydb"
    )

#write main function (test each function and screenshot it)



def add_book( title, author, genre, publication_year, avaiable_copies):
    db = connect_to_db()
    cursor = db.cursor()
    query = """
        INSERT INTO Books (title, author, genre, publicationYear, AvaiableCopies)
        VALUES (%s,%s,%s,%s,%s)
    """
    values = ( title, author, genre, publication_year, avaiable_copies)
    cursor.execute(query,values)
    db.commit()
    print(f"book '{title}' added successfully!")
    cursor.close()
    db.close()

add_book("The Catcher in the Rye", "J.D. Salinger", "Fiction", 1951,5)

def update_book_copies(book_ID, new_Copies):
    db = connect_to_db()
    cursor = db.cursor()
    query = """
        UPDATE Books SET AvaiableCopies = %s WHERE Bookid = %s
    """
    values = (new_Copies, book_ID)
    cursor.execute(query,values)
    db.commit()
    print(f"Book ID {book_ID} updated to {new_Copies} avaiable copies.")
    cursor.close()
    db.close()

update_book_copies(1, 10)

def delete_book(book_ID):
    db = connect_to_db()
    cursor = db.cursor()
    query = """
        DELETE FROM Books WHERE Bookid = %s
    """


    cursor.execute(query, [book_ID])
    db.commit()
    print(f"BookID {book_ID} deleted succesfully!")
    cursor.close()
    db.close()

delete_book(1)

def add_member(name, email, phone_number,membership_Start, membership_End):
    db = connect_to_db()
    cursor = db.cursor()
    query = """
        INSERT INTO members(name, email, phoneNumber,membershipStartDate, membershipEndDate)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (name, email, phone_number, membership_Start, membership_End)
    cursor.execute(query,values)
    db.commit()
    print(f"Member '{name}' added succesfully!")
    cursor.close()
    db.close()

add_member("John Doe", "johndoe@example.com", "123-456-7890", "2024-01-01", "2024-12-31")


def update_member_end_date(member_ID,new_end_date):
    db = connect_to_db()
    cursor = db.cursor()
    query = """
        UPDATE members SET membershipEndDate = %s WHERE memberID = %s
    """
    values = (new_end_date, member_ID)
    cursor.execute(query, values)
    db.commit()
    print(f"Member ID {member_ID} update with new end date {new_end_date}.")
    cursor.close()
    db.close()

update_member_end_date(1, "2024-12-31")
    
def delete_member(member_ID):
    db = connect_to_db()
    cursor = db.cursor()
    query = """
        DELETE FROM members WHERE MemberID = %s
    """
    cursor.execute(query, [member_ID])
    print(f"Member Id {member_ID} deleted succesfully")
    cursor.close()
    db.close()

delete_member(1)

def borrow_book(book_ID, member_ID):
    db = connect_to_db()
    cursor = db.cursor()

    #check if the book is avaiable
    query = """
        SELECT AvaiableCopies FROM books WHERE Bookid = %s
    """
    cursor.execute(query,[book_ID])
    result = cursor.fetchone()
    if result[0] > 0:
        #i am not sure what to do here. i am trying to tell the code by comparing how many copies it has and trying to subtract it while keeping the data of when the book was borrowed
        avaiable_copies = result[0]

        #borrowing in barrowedbook
        borrow_date = date.today()
        query = """
            INSERT INTO borrowedBooks (BookID, MemberID, BorrowDate, IsReturned)
            VALUES(%s,%s,%s,FALSE)
        """
        cursor.execute(query, (book_ID, member_ID, borrow_date))
        db.commit()
        borrow_id = cursor.lastrowid

        #decrease the number of books
        query = """
            UPDATE books SET AvaiableCopies = AvaiableCopies - 1 
            WHERE Bookid = %s
        """
        cursor.execute(query, [book_ID])
        db.commit()

        #log into transaction
        query = """
            INSERT INTO transaction (BorrowID, TransactionDate)
            VALUES (%s, %s)
        """
        cursor.execute(query, [borrow_id, borrow_date])
        db.commit()

        print(f"Book ID {book_ID} borrowed by Member ID {member_ID} on {borrow_date}.")
    else:
        print("No avaiable copies for this book")
    
    cursor.close()
    db.close()

borrow_book(2,4)

def return_book(borrow_ID):
    db = connect_to_db()
    cursor = db.cursor(buffered = True)

    #checking if the book exist or not
    query = """
        SELECT BookID FROM BorrowedBooks WHERE BorrowID = %s AND IsReturned = FALSE
    """
    result = cursor.execute(query, [borrow_ID])

    if result:
        book_ID = result[0]
        return_date = date.today()

        #Mark that the book has been returned
        query = """
            UPDATE BorrwedBooks
            SET ReturnDate = %s, IsReturned = TRUE
            WHERE BorrowID = %s
        """
        cursor.execute(query, [return_date, borrow_ID])
        db.commit()

        #increase the number of book
        query = """
            UPDATE Books SET AvaiableCopies = AvailableCopies + 1 
            WHERE Bookid = %s
        """
        cursor.execute(query, [book_ID])
        db.commit()

        #record the transacition
        query = """
            INSERT INTO transaction (BorrowID, TransactionDate, TransactionType,)
            VALUES (%s, %s, 'Return')
        """
        cursor.execute(query, [book_ID,return_date])
        db.commit()

        print(f"Book ID {book_ID} returned on {return_date}.")
    else:
        print("Invalid borrow ID or the book has been already returned")

    cursor.close()
    db.close()

return_book(4)

def search_book_by_title(title = None):
    db = connect_to_db()
    cursor = db.cursor(buffered = True)

    query = """
        SELECT * FROM Books WHERE title = %s
    """
    result = cursor.execute(query, [title])
    print(result)
    cursor.close()
    db.close()

def search_book_by_author(author = None):
    db = connect_to_db()
    cursor = db.cursor(buffered = True)
    query = """
        SELECT * FROM Books WHERE author = %s
    """
    result = cursor.execute(query, [author])
    print(result)
    cursor.close()
    db.close()

def search_book_by_genre(genre = None):
    db = connect_to_db()
    cursor = db.cursor(buffered = True)

    query = """
        SELECT * FROM Books WHERE genre = %s
    """
    result = cursor.execute(query, [genre])
    print(result)
    cursor.close()
    db.close()


# def search_book(title = None, author = None, genre = None):
#     db = connect_to_db()
#     cursor = db.cursor()

#     query = """
#         SELECT *  FROM Books WHERE 1 = 
#     """
#     values = [ ]

#     if title:
#         query += "AND Title LIKE %s"
#         values.append(f"%[title]%")

#     if author:
#         query += "AND Author LIKE %s"
#         values.append(f"%[author]%")
    
#     if genre:
#         query += "AND Genre LIKE %s"
#         values.append(f"%[Genre]%")
    
#     cursor.execute(query, values)
#     results = cursor.fetchall()

#     #result for book search
#     if results:
#         print("Books Found")
#         for row in results:
#             print(row)
#     else:
#         print("Book has not been found under this criteria")
    
#     cursor.close()
#     db.close()

search_book_by_title(title="The Great Gatsby")
search_book_by_author(author="F. Scott Fitzgerald")
search_book_by_genre(genre="Fiction")
#search_book(title="The Great Gatsby", author="F. Scott Fitzgerald")

# def filter_active_member():
#     db = connect_to_db()
#     cursor = db.cursor()

#     query = """
#         SELECT * From Members 
#         WHERE MembershipEndDate >= %s
#     """

#     cursor_date = date.today()
#     cursor.execute(query, [cursor_date])

#     results = [cursor.fetchall]

#     if results:
#         print("Active Members")
#         for row in results:
#             print(row)
#     else:
#         print("Not an active member")

#     cursor.close()
#     db.close()

# filter_active_member()

import csv

def generate_overdue_books_report():
    db = connect_to_db()
    cursor = db.cursor()

    #define the books overdue after 30days
    overdue_period = timedelta(days=30)
    overdue_date = date.today() - overdue_period

    query = """
        SELECT books.title, borrowDate FROM borrowedBooks
        JOIN books ON books.Bookid = BorrowedBooks.BookID
        WHERE DATEDIFF(borrowDate, %s)>0
    """
        # SELECT MemberName FROM Members
        # SELECT title FROM books
        # SELECT borrowDate FROM BorrowedBooks
        # # SELECT FROM  Members.Name AS MemberName, book.title AS BookTitle, BorrowedBooks.BorrowDate
        # # FROM BorrowedBooks
        # JOIN Books ON BorrowedBooks.BookID = Books.BookID
        # JOIN Members ON BorrowedBooks.MemberID = Members.MemberID
        # WHERE BorrowedBooks.IsReturned = FALSE
        # AND BorrowedBooks.BorrowDate < %s
    
    cursor.execute(query, [overdue_date])

    overdue_books = [cursor.fetchall()]

    if overdue_books:
        print("Overdue books:")
        for row in overdue_books:
            print(row)
    else:
        print("No overdue books")
    
    cursor.close()
    db.close()

    return overdue_books

overdue_books = generate_overdue_books_report()


#def export_overdue_books_report_to_csv(overdue_books):
    #filename = "overdue_books_report.csv"

    #header = ["Member Name", "Book Title", "Borrow Date"]

    #with open(filename, mode = "w", newline == "") as file:
        #writer = csv.writer(file)
        #writer.writerow(header)
        #writer.writerows(overdue_books)
    #print(f"Overdue books report has been export to {filename}")

# def main():
#     search_book_by_genre(genre="Fiction")

# main() 