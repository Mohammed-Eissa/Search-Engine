namespace Search_Engine.Models
{
    public class SearchResult
    {
        public string Url { get; set; } = string.Empty;
        public string Word { get; set; } = string.Empty;
        public int Frequency { get; set; }
        public double PageRank { get; set; }
    }
}
