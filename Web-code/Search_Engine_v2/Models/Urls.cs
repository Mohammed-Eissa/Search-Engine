using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace Search_Engine.Models;
[Table("URLs")]
public class Urls
{
    [Key]
    [Column("URL_ID")]
    public int URL_ID { get; set; }

    [Column("URL")]
    public string URL { get; set; } = string.Empty;

    [Column("PageRank")]
    public double PageRank { get; set; }

}
