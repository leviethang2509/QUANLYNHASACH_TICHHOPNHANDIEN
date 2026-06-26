using System.Data.Entity;

namespace Mood.EF2
{
    public class LogDbContext : DbContext
    {
        public LogDbContext() : base("name=DefaultConnection")
        {
        }

        public DbSet<FaceAuthLog> FaceAuthLogs { get; set; }
        public DbSet<GeofenceLog> GeofenceLogs { get; set; }
        public DbSet<RentalLog> RentalLogs { get; set; }

        protected override void OnModelCreating(DbModelBuilder modelBuilder)
        {
            modelBuilder.Entity<FaceAuthLog>().ToTable("FaceAuthLogs");
            modelBuilder.Entity<GeofenceLog>().ToTable("GeofenceLogs");
            modelBuilder.Entity<RentalLog>().ToTable("RentalLogs");

            base.OnModelCreating(modelBuilder);
        }
    }
}
