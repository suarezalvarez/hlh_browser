import sqlalchemy
from sqlalchemy import text

# Connect to the MySQL server using the root user
root_engine = sqlalchemy.create_engine("mysql+pymysql://root:1234@localhost:3306")

# Create a new database
with root_engine.connect() as connection:
    connection.execute(text("CREATE DATABASE IF NOT EXISTS hlh"))

    # Create a new user
    connection.execute(text("CREATE USER 'hlh_user'@'%' IDENTIFIED BY 'hlh_password'"))

    # Grant privileges to the new user on the database
    connection.execute(text("GRANT ALL PRIVILEGES ON hlh.* TO 'hlh_user'@'%'"))

    #Flush privileges to apply changes
    connection.execute(text("FLUSH PRIVILEGES"))

# Disconnect from the root connection
root_engine.dispose()

