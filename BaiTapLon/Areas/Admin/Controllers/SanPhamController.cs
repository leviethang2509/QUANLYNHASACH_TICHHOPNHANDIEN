using ClosedXML.Excel;
using Mood.Draw;
using Mood.EF2;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace BaiTapLon.Areas.Admin.Controllers
{
    public class SanPhamController : BaseController
    {
        // GET: Admin/SanPham
        public ActionResult Index(string searhString, int page = 1, int pagesize =5)
        {
            var model = new SanphamDraw().listTheloai(searhString, page, pagesize);
            return View(model);
        }
        public ActionResult LocSach(string searhString, int page = 1, int pagesize = 5)
        {
            var model = new SanphamDraw().sachcu(searhString, page, pagesize);
            return View(model);
        }
        public ActionResult LocSachHetHang(string searhString, int page = 1, int pagesize = 5)
        {
            var model = new SanphamDraw().hetHang(searhString, page, pagesize);
            return View(model);
        }
        public ActionResult TaoDon(string searhString, int page = 1, int pagesize = 5)
        {
            var model = new SanphamDraw().listProduct(searhString, page, pagesize);
            return View(model);
        }
        public ActionResult KhoHang(string searhString, int page = 1, int pagesize = 5) {
            var model = new SanphamDraw().listKhoHang(searhString, page, pagesize);
            return View(model);
            
        }
        public ActionResult ThongKeKho(string fromDate, string todate)
        {
            var thongkeList = new SanphamDraw().dataThongKe(fromDate, todate);

            List<string> listNameProduct = new List<string>();
            List<int> listSoLuong = new List<int>();
            List<int> listTonKho = new List<int>();
            foreach (var item in thongkeList)
            {
                listNameProduct.Add(item.Name);
                listSoLuong.Add(item.Soluong);
                listTonKho.Add((int)item.TonKho);
            }
            ViewBag.listNameProduct = listNameProduct;
            ViewBag.listSoLuong = listSoLuong;
            ViewBag.listTonKho = listTonKho;
            ViewBag.fromDate = fromDate;
            ViewBag.todate = todate;
            return View();
        }
        public ActionResult ExportExelTonKho(string fromDate, string toDate)
        {
            //C:/Inetpub/vhosts/hieusachviet.site/httpdocs/
            //D:/Jquery/Do_An/BaiTapLon/
            var wb = new XLWorkbook(@"D:/Jquery/Do_An/BaiTapLon/Resource/Template/Tempalet_Kho_Hang.xlsx");
            var workSheet = wb.Worksheet(1);
            

            var list = new SanphamDraw().dataThongKe(fromDate, toDate);

            workSheet.Cell("D6").Value = DateTime.Now;


            workSheet.Cell("B16").Value = fromDate;


            workSheet.Cell("D16").Value = toDate;

            int row = 19;

            foreach (var item in list)
            {

                workSheet.Cell("B" + row).Value = item.Name;
                workSheet.Cell("C" + row).Value = item.Soluong;
                workSheet.Cell("D" + row).Value = item.TonKho;
                row++;
            }
            string nameFile = "";
            if (!string.IsNullOrEmpty(fromDate) || !string.IsNullOrEmpty(toDate))
            {
                nameFile = "Export_Kho_Hang_Tu_" + fromDate + "_" + toDate + "_" + DateTime.Now.Ticks + ".xlsx";
            }
            else
            {
                nameFile = "Export_Tat_Ca_Kho_Hang" + "_" + DateTime.Now.Ticks + ".xlsx";
            }

            string pathFile = Server.MapPath("~/Resource/ExportFile/" + nameFile);
            try
            {
                wb.SaveAs(pathFile);
            }
            catch
            {
                ViewBag.Error("ÉO LƯU DCD");
            }
            return Json(nameFile, JsonRequestBehavior.AllowGet);

        }
        [HttpGet]
        public ActionResult Create()
        {
            SetViewBag();
            
            return View();
        }
        
        [HttpPost]
        public ActionResult Create(Sanpham sp, HttpPostedFileBase reviewFile)
        {
            if (ModelState.IsValid)
            {
                var draw = new SanphamDraw();
                if(draw.CheckName(sp.Name) == true)
                {
                    SaveReviewFile(reviewFile, sp);
                    if (!ModelState.IsValid)
                    {
                        SetViewBag(sp.CategoryID);
                        return View("Create");
                    }
                    sp.NgayTao = DateTime.Now;
                    sp.Tophot = 1;
                    sp.Soluong = 0;
                    sp.TonKho = 0;
                    
                    var result = draw.Insert(sp);
                    if(result > 0)
                    {
                        ModelState.AddModelError("SanphamSuccess", "Thêm sách thành công");
                    }
                    else
                    {
                        ModelState.AddModelError("Sanpham", "Thêm sách thất bại!!!");
                    }
                }
                else
                {
                    ModelState.AddModelError("Sanpham", "Tên sách đã tồn tại !!!");
                }
            }
            else
            {
                ModelState.AddModelError("Sanpham", "Không thể thêm sách !!!");
            }
            SetViewBag();// ko làm j nó vẫn có danh sách
           
            return View("Create");
        }
        [HttpGet]
        public ActionResult Edit(long id)
        {
            var draw = new SanphamDraw();
            var sanpham = draw.getByID(id);
            if (sanpham == null)
            {
                return RedirectToAction("Index");
            }
            SetViewBag(sanpham.CategoryID);// vào cái nó nhận ngay id của cái đó truyền xuống set viewBag
           
            return View(sanpham);
        }
        [HttpPost]
        public ActionResult Edit(Sanpham sp, HttpPostedFileBase reviewFile)
        {
            if (ModelState.IsValid)
            {
                var draw = new SanphamDraw();
                var current = draw.getByID(sp.IDContent);
                if (current != null && (reviewFile == null || reviewFile.ContentLength <= 0))
                {
                    sp.ReviewFilePath = current.ReviewFilePath;
                    sp.ReviewFileName = current.ReviewFileName;
                }
                SaveReviewFile(reviewFile, sp);
                if (!ModelState.IsValid)
                {
                    SetViewBag(sp.CategoryID);
                    return View("Edit", sp);
                }
                var result = draw.Update(sp);
                if(result)
                {
                    ModelState.AddModelError("SanphamSuccess", "Cập nhật thông tin thành công");
                    var updated = draw.getByID(sp.IDContent) ?? sp;
                    SetViewBag(updated.CategoryID);
                    return View("Edit", updated);
                }
                else
                {
                    var reason = string.IsNullOrWhiteSpace(draw.LastError) ? "" : " Lỗi: " + draw.LastError;
                    ModelState.AddModelError("Sanpham", "Cập nhật thông tin thất bại." + reason);
                }
            }
            else
            {
                ModelState.AddModelError("Sanpham", "Không thể cập nhật thông tin !!!");
            }
            SetViewBag(sp.CategoryID);
           
            return View("Edit", sp);
        }
        [HttpDelete]
        public ActionResult Delete(long id)
        {
            new SanphamDraw().Delete(id);
            return View();
        }
        public void SetViewBag(long? selectedId=null)// có thể null ko truyền j
        {
            // gan viewBag cho category
            var dao = new CategoryDraw();
            ViewBag.CategoryID = new SelectList(dao.ListAll(), "IDCategory", "TenTheloai", selectedId);// bên trong chưa 3 tham số list, giá trị ID, tên hiển thị
        }

        private void SaveReviewFile(HttpPostedFileBase file, Sanpham sp)
        {
            if (file == null || file.ContentLength <= 0) return;

            var extension = (Path.GetExtension(file.FileName) ?? string.Empty).ToLowerInvariant();
            var allowed = new[] { ".pdf", ".jpg", ".jpeg", ".png", ".doc", ".docx", ".md", ".txt" };
            if (!allowed.Contains(extension))
            {
                ModelState.AddModelError("Sanpham", "File review chỉ hỗ trợ PDF, ảnh, Word, Markdown hoặc TXT.");
                return;
            }

            var folder = Server.MapPath("~/Resource/ProductReviews");
            if (!Directory.Exists(folder))
            {
                Directory.CreateDirectory(folder);
            }

            var safeName = Path.GetFileNameWithoutExtension(file.FileName);
            foreach (var c in Path.GetInvalidFileNameChars())
            {
                safeName = safeName.Replace(c, '-');
            }

            safeName = TruncateFileNamePart(safeName, 180);
            var fileName = DateTime.Now.Ticks + "_" + safeName + extension;
            file.SaveAs(Path.Combine(folder, fileName));
            sp.ReviewFilePath = "/Resource/ProductReviews/" + fileName;
            sp.ReviewFileName = TruncateFileName(Path.GetFileName(file.FileName), 250);
        }

        private static string TruncateFileNamePart(string value, int maxLength)
        {
            value = string.IsNullOrWhiteSpace(value) ? "review" : value.Trim();
            return value.Length <= maxLength ? value : value.Substring(0, maxLength);
        }

        private static string TruncateFileName(string fileName, int maxLength)
        {
            if (string.IsNullOrWhiteSpace(fileName)) return fileName;
            if (fileName.Length <= maxLength) return fileName;

            var extension = Path.GetExtension(fileName);
            var name = Path.GetFileNameWithoutExtension(fileName);
            var maxNameLength = Math.Max(1, maxLength - extension.Length);
            return name.Substring(0, Math.Min(name.Length, maxNameLength)) + extension;
        }
    }
}
