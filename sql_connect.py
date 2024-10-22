import sys
import mysql.connector

class sql_connector():
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(host="localhost", user="root", password="", database="stocktrack")
            self.mycursor = self.conn.cursor()
        except Exception as e:
            print("Some error occurred:", e)
            sys.exit(0)

    def register(self, firstname, lastname, email, password):
        try:
            self.mycursor.execute("""
                INSERT INTO users (firstname, lastname, email, password) 
                VALUES (%s, %s, %s, %s);
            """, (firstname, lastname, email, password))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def login(self, email, password):
        try:
            self.mycursor.execute("""
                SELECT * FROM users 
                WHERE email = %s AND password = %s;
            """, (email, password))
            data = self.mycursor.fetchall()
            return data
        except Exception as e:
            print(f"Error: {e}")
            return False


    def insert_portfolio(self, user_id, symbol):
        try:
            self.mycursor.execute("""
                INSERT INTO portfolio(user_id, symbol)
                VALUES(%s, %s);
            """, (user_id, symbol))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        
    def delete_user(self, user_id):
        try:

            self.mycursor.execute("""
                DELETE FROM users WHERE id = %s;
            """, (user_id,))
            self.conn.commit()
            print(f"User with ID {user_id} has been deleted.")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def delete_company_from_portfolio(self, user_id, symbol):
        try:

            self.mycursor.execute("""
                DELETE FROM portfolio WHERE user_id = %s AND symbol = %s;
            """, (user_id, symbol))
            self.conn.commit()
            print(f"Company {symbol} has been removed from user {user_id}'s portfolio.")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        
    def search_portfolio(self, user_id):
        try:
            # Query to get all details from portfolio, stock_price, financial_metric, and news_article
            self.mycursor.execute("""
                SELECT p.symbol, 
                    c.name, 
                    c.sector, 
                    c.industry, 
                    c.description,
                    sp.date, 
                    sp.open, 
                    sp.high, 
                    sp.low, 
                    sp.close, 
                    sp.volume,
                    fm.quarter, 
                    fm.revenue, 
                    fm.earnings, 
                    fm.dividends,
                    na.title, 
                    na.content, 
                    na.published_date
                FROM portfolio p
                JOIN company c ON p.symbol = c.symbol
                LEFT JOIN stock_price sp ON p.symbol = sp.symbol
                LEFT JOIN financial_metric fm ON p.symbol = fm.symbol
                LEFT JOIN news_article na ON p.symbol = na.symbol
                WHERE p.user_id = %s;
            """, (user_id,))

            # Fetch all results
            results = self.mycursor.fetchall()

            # Check if there are any results
            if results:
                return results  # Return all details found
            else:
                print("No companies found in the portfolio for this user.")
                return None

        except Exception as e:
            print(f"Error: {e}")
            return None

