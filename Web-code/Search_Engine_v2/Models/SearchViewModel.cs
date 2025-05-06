namespace Search_Engine.Models
{
    public class SearchViewModel
    {
        public string Query { get; set; } = string.Empty;
        public List<SearchResult> FrequencyResults { get; set; } = new List<SearchResult>();
        public List<SearchResult> PageRankResults { get; set; } = new List<SearchResult>();
    }
}
