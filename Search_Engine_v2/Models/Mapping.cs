using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Search_Engine.Models;

[Table("Mapping")]
public class Mapping
{
    [Key]
    [Column("Mapping_ID")]
    public int Mapping_ID { get; set; }

    [Column("Word_ID")]
    public int Word_ID { get; set; }

    [Column("URL_ID")]
    public int URL_ID { get; set; }

    [Column("Frequency")]
    public int Frequency { get; set; }

    // Navigation properties
    [ForeignKey("Word_ID")]
    public virtual Word? Word { get; set; }

    [ForeignKey("URL_ID")]
    public virtual Urls? Url { get; set; }
}