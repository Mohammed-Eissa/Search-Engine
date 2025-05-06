using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace Search_Engine.Models;
[Table("Word")]
public class Word
{
    [Key]
    [Column("Word_ID")]
    public int Word_ID { get; set; }

    [Column("Word")]
    public string Text { get; set; } = string.Empty;

}
