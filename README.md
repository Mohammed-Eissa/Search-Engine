# Search Engine

A simple web search engine built with ASP.NET Core that ranks results by word frequency and PageRank.

## About This Project

This search engine lets you:
- Search for keywords
- View results ranked by how often words appear (Frequency)
- View results ranked by page importance (PageRank)
- Get clean, user-friendly search results

## How to Run the Project

### What You'll Need
- .NET 6 SDK or newer
- Visual Studio 2022 or Visual Studio Code

### Quick Start Guide

1. **Get the code**
   ```
   git clone https://github.com/Mohammed-Eissa/Search-Engine.git
   ```
   Or download the ZIP file from GitHub

2. **Open the project**
   - If using Visual Studio: Open the .sln file
   - If using VS Code: Open the folder

3. **Run the application**
   - In Visual Studio: Press F5 or click the Run button
   - In terminal/command prompt:
     ```
     dotnet run
     ```

4. **Use the search engine**
   - Open your browser to the URL shown in the terminal (usually http://localhost:5000)
   - Type search terms in the box and click Search
   - View your results!

## How It Works

When you search:
1. The app looks for your keywords in its database
2. It ranks the results in two ways:
   - By how many times the word appears on a page
   - By how important the page is (PageRank algorithm)
3. The results appear in two tables side by side

## Technologies Used

- ASP.NET Core MVC
- Bootstrap for styling
- JavaScript for interactive features

## Contact

Mohammed Eissa - [GitHub Profile](https://github.com/Mohammed-Eissa)

Project Link: [https://github.com/Mohammed-Eissa/Search-Engine](https://github.com/Mohammed-Eissa/Search-Engine)