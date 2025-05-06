using Microsoft.EntityFrameworkCore;
using Search_Engine.Models;

namespace Search_Engine.Data;

public class SearchEngineContext : DbContext
{
    public SearchEngineContext(DbContextOptions<SearchEngineContext> options): base(options)
    {
    }

    public DbSet<Urls> Urls => Set<Urls>();
    public DbSet<Word> Words => Set<Word>();
    public DbSet<Mapping> Mappings => Set<Mapping>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Configure table names to match existing database
        modelBuilder.Entity<Urls>().ToTable("URLs");
        modelBuilder.Entity<Word>().ToTable("Word");
        modelBuilder.Entity<Mapping>().ToTable("Mapping");
        // Configure relationships
        modelBuilder.Entity<Mapping>()
            .HasOne(m => m.Word)
            .WithMany()
            .HasForeignKey(m => m.Word_ID);

        modelBuilder.Entity<Mapping>()
            .HasOne(m => m.Url)
            .WithMany()
            .HasForeignKey(m => m.URL_ID);
    }
}