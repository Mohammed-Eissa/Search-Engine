# 🔍 ASP.NET Core Search Engine

A simple web search engine built with ASP.NET Core that ranks results by word frequency and PageRank.

## ✨ Features

- **Dual-ranking system**: Compare results by frequency or PageRank
- **Clean, responsive UI**: User-friendly interface that works on all devices
- **Fast performance**: Optimized for quick search results

## 📋 Example

Here's what the search engine looks like in action:

![Search Engine Example](https://github.com/Mohammed-Eissa/Search-Engine/raw/main/search-example.png)

*Example showing search results for "help" with both frequency and PageRank rankings*

## 📁 Repository Structure

```
Search-Engine/
├── Scraping&Indexing/      # Python scripts for data preparation
│   ├── scraping.py         # Web crawler and PageRank calculator
│	├── requirements.txt    # requirments for running python files
│   ├── inverted_index.py   # Creates searchable index
│   └── InsertDataIntoDB.py # Populates database
│
└── [ASP.NET Core files]    # Main application files
```

## 🚀 Getting Started

### Prerequisites

- .NET 6 SDK or newer
- Visual Studio 2022 or Visual Studio Code
- Python 3.6+ with packages: requests, beautifulsoup4, pyodbc, networkx, pandas
- SQL Server Database

### Setup Process

1. **Clone the repository first**
   ```bash
   git clone https://github.com/Mohammed-Eissa/Search-Engine.git
   cd Search-Engine
   ```
   
2. **Install the required dependencies**
	```bash
   pip install -r Scraping&Indexing/requirements.txt
   ```

3. **Run Python scripts** (in the Scraping&Indexing folder)
	> Update link to scrap from file scraping.py if you want
   ```bash
   cd Scraping&Indexing
   python scraping.py
   python inverted_index.py scraped_pages output_dir
   python InsertDataIntoDB.py
   ```
   > Update database connection in InsertDataIntoDB.py if needed

4. **Configure and run the ASP.NET application for local run**
   - Return to the main directory: `cd ..`
   - Go to .Net folder : `cd Web-code`
   - Update connection string in appsettings.json
   - Open the .sln file in Visual Studio or the folder in VS Code
   - Run the application (F5 in Visual Studio or `dotnet run` in terminal)
   
   **Or U can Run it with docker compose**
	- Return to the main directory: `cd ..`
	- Go to .Net folder : `cd Web-code`
	- run this command
	```
	docker-compose up -d 
	```

## 🧠 How It Works

### Data Pipeline

1. **Web Scraping**: Collects page content and link structure
2. **Inverted Indexing**: Creates a searchable index of words and their locations
3. **PageRank Calculation**: Determines page importance based on link relationships
4. **Database Storage**: Stores all processed data for fast retrieval
5. **Search & Ranking**: Retrieves and ranks results when users search

## 🛠️ Technical Details

- **Backend**: ASP.NET Core MVC
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Data Processing**: Python (BeautifulSoup, NetworkX, Pandas)
- **Data Storage**: SQL Server Database
- **Algorithms**: Inverted Index, PageRank

## 📝 Scraping & Indexing

The Python scripts in the Scraping&Indexing folder prepare data for the search engine:

### `scraping.py`
- Crawls web pages from a seed URL
- Extracts text content and builds link graph
- Calculates PageRank scores
- Saves to text files and CSV

### `inverted_index.py`
- Processes scraped content
- Creates word-to-document mapping with frequencies
- Outputs an inverted index file

### `InsertDataIntoDB.py`
- Creates database tables
- Loads PageRank scores
- Populates database with words, URLs, and mappings

## 📞 Contact

Mohammed Eissa - [GitHub Profile](https://github.com/Mohammed-Eissa)
                 [Linkedin Profile](https://www.linkedin.com/in/mohamed-eissa-80a298264/)

Project Link: [https://github.com/Mohammed-Eissa/Search-Engine](https://github.com/Mohammed-Eissa/Search-Engine)
