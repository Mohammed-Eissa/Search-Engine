import pyodbc
import base64
import csv
import os

# Database connection parameters
SERVER = 'localhost'  # اسم السيرفر أو IP
PORT = '1433'
DATABASE = 'SearchEngine'  # Replace with your database name
USERNAME = 'sa'  # Optional if using Trusted_Connection
PASSWORD = 'Password@123'  # Optional if using Trusted_Connection

# File paths
inverted_index_file = r"D:\inverted_index.txt"
page_rank_file = r"D:\pagerank_results.csv"

# Decode base64 URL
def decode_base64_url(encoded_url):
    try:
        decoded_bytes = base64.b64decode(encoded_url)
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        print(f"Error decoding URL {encoded_url}: {e}")
        return None

# Create database tables
def create_tables(cursor):
    # URLs table
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[URLs]') AND type = 'U')
    BEGIN
        CREATE TABLE [dbo].[URLs] (
            [URL_ID] INT IDENTITY(1,1) PRIMARY KEY,
            [URL] NVARCHAR(1000) NOT NULL UNIQUE,
            [PageRank] FLOAT NULL
        )
    END
    """)
    
    # Word table (renamed from Words)
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Word]') AND type = 'U')
    BEGIN
        CREATE TABLE [dbo].[Word] (
            [Word_ID] INT IDENTITY(1,1) PRIMARY KEY,
            [Word] NVARCHAR(255) NOT NULL UNIQUE
        )
    END
    """)
    
    # Mapping table (renamed from WordURLMapping)
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Mapping]') AND type = 'U')
    BEGIN
        CREATE TABLE [dbo].[Mapping] (
            [Mapping_ID] INT IDENTITY(1,1) PRIMARY KEY,
            [Word_ID] INT NOT NULL,
            [URL_ID] INT NOT NULL,
            [Frequency] INT NOT NULL,
            CONSTRAINT [FK_Mapping_Word] FOREIGN KEY ([Word_ID]) REFERENCES [dbo].[Word] ([Word_ID]),
            CONSTRAINT [FK_Mapping_URLs] FOREIGN KEY ([URL_ID]) REFERENCES [dbo].[URLs] ([URL_ID]),
            CONSTRAINT [UQ_WordURL] UNIQUE ([Word_ID], [URL_ID])
        )
    END
    """)
    
    print("✅ Tables checked/created.")

# Load PageRank CSV
def load_page_rank_data(file_path):
    page_ranks = {}
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) >= 2:
                        url = row[0].strip().rstrip('/')
                        try:
                            rank = float(row[1])
                            page_ranks[url] = rank
                        except ValueError:
                            print(f"⚠ Invalid rank for {url}")
        except Exception as e:
            print(f"⚠ Error reading PageRank file: {e}")
    else:
        print(f"❌ PageRank file not found: {file_path}")
    return page_ranks

# Main data processing
def process_and_insert_data():
    try:
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER},{PORT};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};TrustServerCertificate=yes;'
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Create tables
        create_tables(cursor)

        # Load PageRanks
        page_ranks = load_page_rank_data(page_rank_file)

        # Read inverted index
        with open(inverted_index_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        url_ids = {}
        word_ids = {}

        for line in lines:
            line = line.strip()
            if not line:
                continue

            parts = line.split('\t', 1)
            if len(parts) < 2:
                print(f"⚠ Skipping invalid line: {line}")
                continue

            word = parts[0].strip('"')
            occurrences_data = parts[1]

            # Insert or get Word_ID
            if word not in word_ids:
                cursor.execute("SELECT Word_ID FROM Word WHERE Word = ?", word)
                row = cursor.fetchone()
                if row:
                    word_ids[word] = row[0]
                else:
                    cursor.execute("INSERT INTO Word (Word) VALUES (?)", word)
                    cursor.execute("SELECT @@IDENTITY")
                    word_ids[word] = int(cursor.fetchone()[0])
                conn.commit()

            word_id = word_ids[word]
            occurrences = occurrences_data.split(';')

            for occurrence in occurrences:
                if not occurrence:
                    continue

                occurrence_parts = occurrence.split(':', 1)
                if len(occurrence_parts) < 2:
                    print(f"⚠ Invalid occurrence: {occurrence}")
                    continue

                encoded_url = occurrence_parts[0]
                frequency = int(occurrence_parts[1])

                decoded_url = decode_base64_url(encoded_url)
                if not decoded_url:
                    continue

                normalized_url = decoded_url.strip().rstrip('/')

                # Insert or get URL_ID
                if decoded_url not in url_ids:
                    cursor.execute("SELECT URL_ID FROM URLs WHERE URL = ?", decoded_url)
                    row = cursor.fetchone()
                    if row:
                        url_ids[decoded_url] = row[0]
                    else:
                        page_rank = page_ranks.get(normalized_url, None)
                        cursor.execute("INSERT INTO URLs (URL, PageRank) VALUES (?, ?)", decoded_url, page_rank)
                        cursor.execute("SELECT @@IDENTITY")
                        url_ids[decoded_url] = int(cursor.fetchone()[0])
                        print(f"✅ Inserted URL: {decoded_url} | PageRank: {page_rank}")
                    conn.commit()

                url_id = url_ids[decoded_url]

                # Insert into mapping table
                try:
                    cursor.execute("""
                    MERGE INTO Mapping AS target
                    USING (SELECT ? AS Word_ID, ? AS URL_ID, ? AS Frequency) AS source
                    ON (target.Word_ID = source.Word_ID AND target.URL_ID = source.URL_ID)
                    WHEN MATCHED THEN
                        UPDATE SET Frequency = source.Frequency
                    WHEN NOT MATCHED THEN
                        INSERT (Word_ID, URL_ID, Frequency)
                        VALUES (source.Word_ID, source.URL_ID, source.Frequency);
                    """, word_id, url_id, frequency)
                    conn.commit()
                except Exception as e:
                    print(f"❌ Error inserting mapping for '{word}' and '{decoded_url}': {e}")
                    conn.rollback()

        print("✅ Data inserted successfully.")
    
    except Exception as e:
        print(f"❌ Main Error: {e}")
    
    finally:
        if 'conn' in locals():
            conn.close()

# Run the script
if _name_ == "_main_":
    process_and_insert_data()