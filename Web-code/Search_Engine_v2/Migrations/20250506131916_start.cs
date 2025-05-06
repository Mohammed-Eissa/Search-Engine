using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Search_Engine.Migrations
{
    /// <inheritdoc />
    public partial class start : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "URLs",
                columns: table => new
                {
                    URL_ID = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    URL = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    PageRank = table.Column<double>(type: "float", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_URLs", x => x.URL_ID);
                });

            migrationBuilder.CreateTable(
                name: "Word",
                columns: table => new
                {
                    Word_ID = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Word = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Word", x => x.Word_ID);
                });

            migrationBuilder.CreateTable(
                name: "Mapping",
                columns: table => new
                {
                    Mapping_ID = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Word_ID = table.Column<int>(type: "int", nullable: false),
                    URL_ID = table.Column<int>(type: "int", nullable: false),
                    Frequency = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Mapping", x => x.Mapping_ID);
                    table.ForeignKey(
                        name: "FK_Mapping_URLs_URL_ID",
                        column: x => x.URL_ID,
                        principalTable: "URLs",
                        principalColumn: "URL_ID",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_Mapping_Word_Word_ID",
                        column: x => x.Word_ID,
                        principalTable: "Word",
                        principalColumn: "Word_ID",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_Mapping_URL_ID",
                table: "Mapping",
                column: "URL_ID");

            migrationBuilder.CreateIndex(
                name: "IX_Mapping_Word_ID",
                table: "Mapping",
                column: "Word_ID");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Mapping");

            migrationBuilder.DropTable(
                name: "URLs");

            migrationBuilder.DropTable(
                name: "Word");
        }
    }
}
