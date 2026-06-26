using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using ClosedXML.Excel;
using Mood.Draw;
using Mood.EF2;
using Mood.ThongKeModel;

namespace BaiTapLon.Areas.Admin.Controllers
{
    public class ThongKeController : BaseController
    {
        // GET: Admin/ThongKe
        public ActionResult Index()
        {
            return View();
        }

        public ActionResult ThongKeSanPhamHot()
        {
            ViewBag.listSanPhamHot = new SanphamDraw().listTopSellings(5);
            return View();
        }

        public ActionResult DoanhThu(string fromDate, string todate, int page = 1, int pageSize = 20)
        {
            var thongkeList = new OrderDraw().getDoanhThu(fromDate, todate, page, pageSize);

            int tongThu = 0;
            int tongLai = 0;
            foreach (var item in thongkeList)
            {
                tongThu += (int)item.DoanhThu;
                tongLai += (int)item.TongLai;
            }
            ViewBag.tongThu = tongThu;
            ViewBag.tongLai = tongLai;
            ViewBag.fromDate = fromDate;
            ViewBag.todate = todate;
            return View(thongkeList);
        }

        public ActionResult DoanhThuChart(string fromDate, string todate)
        {
            var thongkeList = new OrderDraw().getDoanhThuChart(fromDate, todate);

            List<int> listDoanhThu = new List<int>();
            List<int> listTongLai = new List<int>();
            List<string> doanhsoNgay = new List<string>();
            int tongThu = 0;
            int tongLai = 0;
            foreach (var item in thongkeList)
            {
                tongThu += (int)item.DoanhThu;
                tongLai += (int)item.TongLai;
                listDoanhThu.Add((int)item.DoanhThu);
                listTongLai.Add((int)item.TongLai);
                doanhsoNgay.Add(item.DoanhThuNgay.ToString("dd/MM/yyyy"));
            }
            ViewBag.listDoanhThu = listDoanhThu;
            ViewBag.listTongLai = listTongLai;
            ViewBag.doanhsoNgay = doanhsoNgay;
            ViewBag.tongThu = tongThu;
            ViewBag.tongLai = tongLai;
            ViewBag.fromDate = fromDate;
            ViewBag.todate = todate;
            return View();
        }

        public ActionResult MuonTraChuDe(string fromDate, string toDate, string status)
        {
            DateTime parsedFromDate;
            DateTime parsedToDate;
            DateTime? from = DateTime.TryParseExact(fromDate, "yyyy-MM-dd", CultureInfo.InvariantCulture, DateTimeStyles.None, out parsedFromDate)
                ? (DateTime?)parsedFromDate.Date
                : null;
            DateTime? toExclusive = DateTime.TryParseExact(toDate, "yyyy-MM-dd", CultureInfo.InvariantCulture, DateTimeStyles.None, out parsedToDate)
                ? (DateTime?)parsedToDate.Date.AddDays(1)
                : null;

            using (var db = new QuanLySachDBContext())
            {
                var query =
                    from rental in db.RentalRequests
                    join product in db.Sanphams on rental.ProductID equals product.IDContent
                    join category in db.Categories on product.CategoryID equals category.IDCategory into categoryJoin
                    from category in categoryJoin.DefaultIfEmpty()
                    select new RentalTopicRaw
                    {
                        CategoryId = product.CategoryID,
                        CategoryName = category != null ? category.TenTheloai : "Chưa phân loại",
                        Status = rental.Status,
                        RequestDate = rental.RequestDate,
                        ExpectedReturnDate = rental.ExpectedReturnDate,
                        Quantity = rental.Quantity
                    };

                if (from.HasValue)
                {
                    query = query.Where(x => x.RequestDate >= from.Value);
                }
                if (toExclusive.HasValue)
                {
                    query = query.Where(x => x.RequestDate < toExclusive.Value);
                }
                if (!string.IsNullOrWhiteSpace(status))
                {
                    query = query.Where(x => x.Status == status);
                }

                var rows = query.ToList();
                var now = DateTime.Now;
                var stats = rows
                    .GroupBy(x => new { x.CategoryId, x.CategoryName })
                    .Select(g => new RentalTopicStat
                    {
                        CategoryId = g.Key.CategoryId,
                        CategoryName = string.IsNullOrWhiteSpace(g.Key.CategoryName) ? "Chưa phân loại" : g.Key.CategoryName,
                        Total = g.Count(),
                        Pending = g.Count(x => x.Status == "Pending"),
                        Borrowing = g.Count(x => x.Status == "Borrowed" || x.Status == "Borrowing" || x.Status == "Approved"),
                        Returned = g.Count(x => x.Status == "Returned"),
                        Overdue = g.Count(x => x.Status == "Overdue" || (x.ExpectedReturnDate < now && x.Status != "Returned" && x.Status != "Rejected" && x.Status != "Cancelled")),
                        Quantity = g.Sum(x => x.Quantity)
                    })
                    .OrderByDescending(x => x.Total)
                    .ToList();

                var trend = rows
                    .GroupBy(x => x.RequestDate.Date)
                    .OrderBy(x => x.Key)
                    .Select(g => new RentalTrendPoint
                    {
                        DateLabel = g.Key.ToString("dd/MM"),
                        Total = g.Count()
                    })
                    .ToList();

                ViewBag.FromDate = fromDate;
                ViewBag.ToDate = toDate;
                ViewBag.Status = status;
                ViewBag.Labels = stats.Select(x => x.CategoryName).Take(10).ToList();
                ViewBag.BorrowTotals = stats.Select(x => x.Total).Take(10).ToList();
                ViewBag.PendingTotal = rows.Count(x => x.Status == "Pending");
                ViewBag.BorrowingTotal = rows.Count(x => x.Status == "Borrowed" || x.Status == "Borrowing" || x.Status == "Approved");
                ViewBag.ReturnedTotal = rows.Count(x => x.Status == "Returned");
                ViewBag.OverdueTotal = rows.Count(x => x.Status == "Overdue" || (x.ExpectedReturnDate < now && x.Status != "Returned" && x.Status != "Rejected" && x.Status != "Cancelled"));
                ViewBag.TrendLabels = trend.Select(x => x.DateLabel).ToList();
                ViewBag.TrendTotals = trend.Select(x => x.Total).ToList();
                return View(stats);
            }
        }

        public ActionResult ExportExel(string fromDate, string toDate)
        {
            var wb = new XLWorkbook(@"D:/Jquery/Do_An/BaiTapLon/Resource/Template/Tempalet_Doanh_Thu.xlsx");
            var workSheet = wb.Worksheet(1);
            if (!string.IsNullOrEmpty(fromDate) || !string.IsNullOrEmpty(toDate))
            {
                workSheet.Cell("C1").Value = "Thông Kê Doanh Thu";
            }
            else
            {
                workSheet.Cell("C1").Value = "Thông Kê Doanh Thu Cả Năm";
            }

            var list = new OrderDraw().getDoanhThuChart(fromDate, toDate);

            workSheet.Cell("D6").Value = DateTime.Now;
            workSheet.Cell("B16").Value = fromDate;
            workSheet.Cell("D16").Value = toDate;

            int row = 19;
            foreach (var item in list)
            {
                workSheet.Cell("B" + row).Value = item.DoanhThuNgay;
                workSheet.Cell("C" + row).Value = item.DoanhThu;
                workSheet.Cell("D" + row).Value = item.TongLai;
                row++;
            }
            string nameFile = "";
            if (!string.IsNullOrEmpty(fromDate) || !string.IsNullOrEmpty(toDate))
            {
                nameFile = "Export_Doanh_Thu_Tu_" + fromDate + "_" + toDate + "_" + DateTime.Now.Ticks + ".xlsx";
            }
            else
            {
                nameFile = "Export_Doanh_Thu_Ca_Nam" + "_" + DateTime.Now.Ticks + ".xlsx";
            }

            string pathFile = Server.MapPath("~/Resource/ExportFile/" + nameFile);
            try
            {
                wb.SaveAs(pathFile);
            }
            catch
            {
                // swallow; preserving runtime stability
            }
            return Json(nameFile, JsonRequestBehavior.AllowGet);
        }

        public class RentalTopicStat
        {
            public long? CategoryId { get; set; }
            public string CategoryName { get; set; }
            public int Total { get; set; }
            public int Pending { get; set; }
            public int Borrowing { get; set; }
            public int Returned { get; set; }
            public int Overdue { get; set; }
            public int Quantity { get; set; }
        }

        private class RentalTopicRaw
        {
            public long? CategoryId { get; set; }
            public string CategoryName { get; set; }
            public string Status { get; set; }
            public DateTime RequestDate { get; set; }
            public DateTime ExpectedReturnDate { get; set; }
            public int Quantity { get; set; }
        }

        private class RentalTrendPoint
        {
            public string DateLabel { get; set; }
            public int Total { get; set; }
        }
    }
}
