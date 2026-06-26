using System;

namespace BaiTapLon.Areas.Admin.Models
{
    public class LogFilterModel<T>
    {
        public T Logs { get; set; }
        public int Page { get; set; }
        public int PageSize { get; set; }
        public int Total { get; set; }
        public long? UserId { get; set; }
        public int? StoreId { get; set; }
        public int? RentalId { get; set; }
        public string Action { get; set; }
        public DateTime? FromDate { get; set; }
        public DateTime? ToDate { get; set; }
        public bool? Result { get; set; }
        public bool? InZone { get; set; }

        public int TotalPages
        {
            get
            {
                if (PageSize <= 0) return 1;
                var pages = (int)Math.Ceiling((double)Total / PageSize);
                return pages < 1 ? 1 : pages;
            }
        }
    }
}
