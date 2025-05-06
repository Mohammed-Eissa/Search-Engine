using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Search_Engine.Models;
using Search_Engine.Data;

namespace Search_Engine.Controllers;

public class SearchController : Controller
{
    private readonly SearchEngineContext _context;
    private readonly ILogger<SearchController> _logger;

    public SearchController(SearchEngineContext context, ILogger<SearchController> logger)
    {
        _context = context;
        _logger = logger;
    }

    // GET: /Search or /
    [Route("/")]
    [Route("/Search")]
    [Route("/Search/Index")]
    public IActionResult Index()
    {
        return View(new SearchViewModel());
    }

    // POST: /Search/Search
    [HttpPost]
    public async Task<IActionResult> Search(string query)
    {
        if (string.IsNullOrWhiteSpace(query))
        {
            return View("Index", new SearchViewModel());
        }

        var searchTerms = query.ToLower().Split(' ', StringSplitOptions.RemoveEmptyEntries);
        var viewModel = new SearchViewModel { Query = query };

        try
        {
            // Find words that match the search terms
            var wordIds = await _context.Words
                .Where(w => searchTerms.Contains(w.Text.ToLower()))
                .Select(w => w.Word_ID)
                .ToListAsync();

            if (!wordIds.Any())
            {
                return View("Index", viewModel);
            }

            // Get all mappings for these words
            var mappings = await _context.Mappings
                .Include(m => m.Word)
                .Include(m => m.Url)
                .Where(m => wordIds.Contains(m.Word_ID))
                .ToListAsync();

            // Group by URL to consolidate results for multiple search terms
            var resultsByUrl = mappings
                .GroupBy(m => m.URL_ID)
                .Select(g => new
                {
                    Url = g.First().Url!,
                    TotalFrequency = g.Sum(m => m.Frequency),
                    Words = g.Select(m => m.Word!.Text).Distinct().ToList()
                })
                .ToList();

            // Create results sorted by frequency (descending)
            viewModel.FrequencyResults = resultsByUrl
                .OrderByDescending(r => r.TotalFrequency)
                .Select(r => new SearchResult
                {
                    Url = r.Url.URL,
                    Word = string.Join(", ", r.Words),
                    Frequency = r.TotalFrequency,
                    PageRank = r.Url.PageRank
                })
                .ToList();

            // Create results sorted by PageRank (descending)
            viewModel.PageRankResults = resultsByUrl
                .OrderByDescending(r => r.Url.PageRank)
                .Select(r => new SearchResult
                {
                    Url = r.Url.URL,
                    Word = string.Join(", ", r.Words),
                    Frequency = r.TotalFrequency,
                    PageRank = r.Url.PageRank
                })
                .ToList();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error occurred while searching for query: {Query}", query);
            ModelState.AddModelError(string.Empty, "An error occurred while processing your search. Please try again.");
        }

        return View("Index", viewModel);
    }
}