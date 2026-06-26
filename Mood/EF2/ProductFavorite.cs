namespace Mood.EF2
{
    using System;
    using System.ComponentModel.DataAnnotations;
    using System.ComponentModel.DataAnnotations.Schema;

    [Table("ProductFavorites")]
    public partial class ProductFavorite
    {
        public long ID { get; set; }

        public long UserID { get; set; }

        public long ProductID { get; set; }

        public DateTime CreatedAt { get; set; }
    }
}
