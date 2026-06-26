using BaiTapLon.Common;
using BaiTapLon.Models;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Wordprocessing;
using Mood.Draw;
using Mood.EF2;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Web;
using System.Web.Mvc;

namespace BaiTapLon.Controllers
{
    public class ProductController : Controller
    {
        // GET: Product
        public ActionResult Index()
        {
            return View();
        }

        [ChildActionOnly]
        public PartialViewResult Category()
        {
            var cart = Session[Constant.CartSession];
            var list = new List<CartItem>();
            if (cart != null)
            {
                list = (List<CartItem>)cart;
            }
            ViewBag.CartList = list.Count;

            var model = new CategoryDraw().ListAllCategory(7);
            ViewBag.Sanphamnew = new SanphamDraw().listSanphamnew(8);
            ViewBag.topHot = new SanphamDraw().listTopSellings(8);
            ViewBag.getAllProduct = new SanphamDraw().getAllProduct();
            return PartialView(model);
        }

        [ChildActionOnly]
        public PartialViewResult CategoryMobile()
        {
            ViewBag.listMenu = new MenuDraw().listAll();
            var model = new CategoryDraw().ListAllCategory(7);
            ViewBag.getAllProduct = new SanphamDraw().getAllProduct();
            return PartialView(model);
        }

        public JsonResult ListName(string q)
        {
            var data = new SanphamDraw().ListName(q);
            return Json(new
            {
                data = data,
                status = true
            }, JsonRequestBehavior.AllowGet);
        }

        public ActionResult Search(string keyWord, int page = 1, int pagesize = 20)
        {
            var model = new SanphamDraw().getByKeyWord(keyWord, page, pagesize);
            ViewBag.totalKq = model.Count();
            ViewBag.keyWord = keyWord;
            ViewBag.listGoiY = new SanphamDraw().listSanphamnew(5);
            ViewBag.total = new SanphamDraw().ListCount();
            ViewBag.Category = new CategoryDraw().ListAll();
            return View(model);
        }

        public ActionResult ListProduct(long? idCate, int page = 1, int pageSize = 20)
        {
            IEnumerable<Sanpham> model;
            if (idCate != null)
            {
                model = new SanphamDraw().getByIDcate(idCate, page, pageSize);
                ViewBag.TenTheLoai = new CategoryDraw().getByID((int)idCate);
            }
            else
            {
                model = new SanphamDraw().listAllProduct(page, pageSize);
            }
            ViewBag.listGoiY = new SanphamDraw().listSanphamnew(5);
            ViewBag.total = new SanphamDraw().ListCount();
            ViewBag.Category = new CategoryDraw().ListAll();
            return View(model);
        }

        public ActionResult Detail(long idDetail)
        {
            var model = new SanphamDraw().getByID(idDetail);
            if (model == null)
            {
                return RedirectToAction("NotFound");
            }

            ViewBag.sanPhamCategory = model.CategoryID.HasValue
                ? new CategoryDraw().getByID(model.CategoryID.Value)
                : null;
            ViewBag.sanPhamLienquan = model.CategoryID.HasValue
                ? new SanphamDraw().getByIDcateDetail(model.CategoryID, idDetail)
                : new List<Sanpham>();

            var reviewDraw = new ProductReviewDraw();
            ViewBag.ProductReviews = reviewDraw.ListByProduct(idDetail);
            ViewBag.ProductReviewCount = reviewDraw.CountByProduct(idDetail);
            ViewBag.ProductAverageRating = reviewDraw.AverageRating(idDetail);
            ViewBag.YoutubeEmbedUrl = BuildYoutubeEmbedUrl(model.YoutubeUrl);
            return View(model);
        }

        public ActionResult ReviewFile(long id)
        {
            var fileInfo = ResolveReviewFile(id);
            if (fileInfo == null)
            {
                return HttpNotFound();
            }

            Response.AddHeader("Content-Disposition", "inline; filename=\"" + fileInfo.FileName.Replace("\"", "") + "\"");
            return File(fileInfo.FullPath, GetReviewContentType(fileInfo.FullPath));
        }

        public ActionResult ReviewFilePreview(long id)
        {
            var fileInfo = ResolveReviewFile(id);
            if (fileInfo == null)
            {
                return HttpNotFound();
            }

            ViewBag.ProductId = id;
            ViewBag.FileName = "Review sách";
            ViewBag.Extension = fileInfo.Extension;
            ViewBag.FileUrl = Url.Action("ReviewFile", "Product", new { id = id });
            ViewBag.DownloadUrl = Url.Action("ReviewFileDownload", "Product", new { id = id });
            ViewBag.PreviewKind = GetPreviewKind(fileInfo.Extension);
            if (IsWordFile(fileInfo.Extension))
            {
                string pdfPath;
                if (TryGetPdfPreview(fileInfo, id, out pdfPath))
                {
                    ViewBag.PreviewKind = "pdf";
                    ViewBag.FileUrl = Url.Action("ReviewPdfPreview", "Product", new { id = id });
                }
                else if (fileInfo.Extension == ".docx")
                {
                    ViewBag.PreviewKind = "docx";
                    ViewBag.DocumentParagraphs = ReadDocxParagraphs(fileInfo.FullPath);
                    ViewBag.PreviewWarning = "Muốn giữ nguyên từng trang như PDF, hãy cài LibreOffice hoặc cấu hình OfficeToPDF để hệ thống tự chuyển Word sang PDF.";
                }
                else
                {
                    ViewBag.PreviewKind = "unsupported";
                    ViewBag.PreviewWarning = "File Word .doc cần bộ chuyển đổi LibreOffice hoặc OfficeToPDF để xem giống PDF.";
                }
            }
            else if ((string)ViewBag.PreviewKind == "text")
            {
                ViewBag.TextContent = System.IO.File.ReadAllText(fileInfo.FullPath, Encoding.UTF8);
            }

            return View();
        }

        public ActionResult ReviewPdfPreview(long id)
        {
            var fileInfo = ResolveReviewFile(id);
            if (fileInfo == null)
            {
                return HttpNotFound();
            }

            string pdfPath;
            if (!TryGetPdfPreview(fileInfo, id, out pdfPath) || !System.IO.File.Exists(pdfPath))
            {
                return HttpNotFound();
            }

            Response.AddHeader("Content-Disposition", "inline; filename=\"review.pdf\"");
            return File(pdfPath, "application/pdf");
        }

        public ActionResult ReviewFileDownload(long id)
        {
            var fileInfo = ResolveReviewFile(id);
            if (fileInfo == null)
            {
                return HttpNotFound();
            }

            return File(fileInfo.FullPath, "application/octet-stream", fileInfo.FileName);
        }

        [HttpPost]
        public ActionResult AddReview(long productId, int rating, string comment)
        {
            var session = Session[Constant.USER_SESSION] as UserLogin;
            if (session == null)
            {
                return Json(new { success = false, requireLogin = true, message = "Vui lòng đăng nhập để đánh giá sách." });
            }

            var success = new ProductReviewDraw().Upsert(new ProductReview
            {
                ProductID = productId,
                UserID = session.userId,
                UserName = session.name,
                Rating = rating,
                Comment = (comment ?? string.Empty).Trim()
            });

            return Json(new
            {
                success,
                message = success ? "Đã lưu đánh giá của bạn." : "Không thể lưu đánh giá. Vui lòng nhập đủ số sao và bình luận."
            });
        }

        private static string BuildYoutubeEmbedUrl(string url)
        {
            if (string.IsNullOrWhiteSpace(url)) return string.Empty;

            Uri uri;
            if (!Uri.TryCreate(url.Trim(), UriKind.Absolute, out uri)) return string.Empty;

            var host = uri.Host.ToLowerInvariant();
            string videoId = string.Empty;
            if (host.Contains("youtu.be"))
            {
                videoId = uri.AbsolutePath.Trim('/');
            }
            else if (host.Contains("youtube.com"))
            {
                var query = HttpUtility.ParseQueryString(uri.Query);
                videoId = query["v"];
                if (string.IsNullOrWhiteSpace(videoId) && uri.AbsolutePath.Contains("/embed/"))
                {
                    videoId = uri.AbsolutePath.Split(new[] { "/embed/" }, StringSplitOptions.None).Last();
                }
            }

            return string.IsNullOrWhiteSpace(videoId)
                ? string.Empty
                : "https://www.youtube.com/embed/" + HttpUtility.UrlEncode(videoId);
        }

        private static string GetReviewContentType(string path)
        {
            switch ((Path.GetExtension(path) ?? string.Empty).ToLowerInvariant())
            {
                case ".pdf": return "application/pdf";
                case ".jpg":
                case ".jpeg": return "image/jpeg";
                case ".png": return "image/png";
                case ".md":
                case ".txt": return "text/plain; charset=utf-8";
                case ".doc": return "application/msword";
                case ".docx": return "application/vnd.openxmlformats-officedocument.wordprocessingml.document";
                default: return "application/octet-stream";
            }
        }

        private ReviewFileInfo ResolveReviewFile(long id)
        {
            var product = new SanphamDraw().getByID(id);
            if (product == null || string.IsNullOrWhiteSpace(product.ReviewFilePath))
            {
                return null;
            }

            var relativePath = product.ReviewFilePath.StartsWith("~")
                ? product.ReviewFilePath
                : "~/" + product.ReviewFilePath.TrimStart('/');
            var fullPath = Server.MapPath(relativePath);
            if (!System.IO.File.Exists(fullPath))
            {
                return null;
            }

            return new ReviewFileInfo
            {
                FullPath = fullPath,
                FileName = string.IsNullOrWhiteSpace(product.ReviewFileName)
                    ? Path.GetFileName(fullPath)
                    : product.ReviewFileName,
                Extension = (Path.GetExtension(fullPath) ?? string.Empty).ToLowerInvariant()
            };
        }

        private static string GetPreviewKind(string extension)
        {
            switch ((extension ?? string.Empty).ToLowerInvariant())
            {
                case ".pdf": return "pdf";
                case ".jpg":
                case ".jpeg":
                case ".png": return "image";
                case ".md":
                case ".txt": return "text";
                case ".docx": return "docx";
                case ".doc": return "word";
                default: return "unsupported";
            }
        }

        private bool TryGetPdfPreview(ReviewFileInfo fileInfo, long productId, out string pdfPath)
        {
            pdfPath = null;
            if (fileInfo.Extension == ".pdf")
            {
                pdfPath = fileInfo.FullPath;
                return true;
            }
            if (!IsWordFile(fileInfo.Extension))
            {
                return false;
            }

            var previewFolder = Server.MapPath("~/Resource/ProductReviewPreviews");
            Directory.CreateDirectory(previewFolder);

            var sourceVersion = System.IO.File.GetLastWriteTimeUtc(fileInfo.FullPath).Ticks;
            pdfPath = Path.Combine(previewFolder, productId + "_" + sourceVersion + ".pdf");
            if (System.IO.File.Exists(pdfPath))
            {
                return true;
            }

            DeleteOldPreviewFiles(previewFolder, productId);
            return TryConvertWithLibreOffice(fileInfo.FullPath, previewFolder, pdfPath)
                || TryConvertWithOfficeToPdf(fileInfo.FullPath, pdfPath);
        }

        private static bool IsWordFile(string extension)
        {
            extension = (extension ?? string.Empty).ToLowerInvariant();
            return extension == ".doc" || extension == ".docx";
        }

        private static void DeleteOldPreviewFiles(string previewFolder, long productId)
        {
            foreach (var path in Directory.GetFiles(previewFolder, productId + "_*.pdf"))
            {
                try { System.IO.File.Delete(path); } catch { }
            }
        }

        private bool TryConvertWithLibreOffice(string inputPath, string outputFolder, string expectedPdfPath)
        {
            var sofficePath = ResolveConfiguredOrKnownPath("ReviewLibreOfficePath", new[]
            {
                @"C:\Program Files\LibreOffice\program\soffice.exe",
                @"C:\Program Files (x86)\LibreOffice\program\soffice.exe"
            });
            if (string.IsNullOrWhiteSpace(sofficePath)) return false;

            var startInfo = new ProcessStartInfo
            {
                FileName = sofficePath,
                Arguments = "--headless --convert-to pdf --outdir \"" + outputFolder + "\" \"" + inputPath + "\"",
                CreateNoWindow = true,
                UseShellExecute = false,
                RedirectStandardError = true,
                RedirectStandardOutput = true
            };

            return RunConversionProcess(startInfo, Path.Combine(outputFolder, Path.GetFileNameWithoutExtension(inputPath) + ".pdf"), expectedPdfPath);
        }

        private bool TryConvertWithOfficeToPdf(string inputPath, string expectedPdfPath)
        {
            var officeToPdfPath = ResolveConfiguredOrKnownPath("ReviewOfficeToPdfPath", new[]
            {
                Server.MapPath("~/bin/OfficeToPDF.exe"),
                Server.MapPath("~/App_Data/Tools/OfficeToPDF.exe")
            });
            if (string.IsNullOrWhiteSpace(officeToPdfPath)) return false;

            var startInfo = new ProcessStartInfo
            {
                FileName = officeToPdfPath,
                Arguments = "\"" + inputPath + "\" \"" + expectedPdfPath + "\"",
                CreateNoWindow = true,
                UseShellExecute = false,
                RedirectStandardError = true,
                RedirectStandardOutput = true
            };

            return RunConversionProcess(startInfo, expectedPdfPath, expectedPdfPath);
        }

        private static bool RunConversionProcess(ProcessStartInfo startInfo, string producedPdfPath, string expectedPdfPath)
        {
            try
            {
                using (var process = Process.Start(startInfo))
                {
                    if (process == null) return false;
                    if (!process.WaitForExit(60000))
                    {
                        try { process.Kill(); } catch { }
                        return false;
                    }
                }

                if (!System.IO.File.Exists(producedPdfPath)) return false;
                if (!string.Equals(producedPdfPath, expectedPdfPath, StringComparison.OrdinalIgnoreCase))
                {
                    if (System.IO.File.Exists(expectedPdfPath)) System.IO.File.Delete(expectedPdfPath);
                    System.IO.File.Move(producedPdfPath, expectedPdfPath);
                }

                return System.IO.File.Exists(expectedPdfPath);
            }
            catch
            {
                return false;
            }
        }

        private static string ResolveConfiguredOrKnownPath(string appSettingKey, IEnumerable<string> knownPaths)
        {
            var configuredPath = ConfigurationManager.AppSettings[appSettingKey];
            if (!string.IsNullOrWhiteSpace(configuredPath) && System.IO.File.Exists(configuredPath))
            {
                return configuredPath;
            }

            return knownPaths.FirstOrDefault(System.IO.File.Exists);
        }

        private static List<string> ReadDocxParagraphs(string path)
        {
            var paragraphs = new List<string>();
            try
            {
                using (var document = WordprocessingDocument.Open(path, false))
                {
                    var body = document.MainDocumentPart != null && document.MainDocumentPart.Document != null
                        ? document.MainDocumentPart.Document.Body
                        : null;
                    if (body == null) return paragraphs;

                    foreach (var paragraph in body.Descendants<Paragraph>())
                    {
                        var text = string.Concat(paragraph.Descendants<Text>().Select(x => x.Text)).Trim();
                        if (!string.IsNullOrWhiteSpace(text))
                        {
                            paragraphs.Add(text);
                        }
                    }
                }
            }
            catch
            {
                paragraphs.Clear();
            }

            return paragraphs;
        }

        private class ReviewFileInfo
        {
            public string FullPath { get; set; }
            public string FileName { get; set; }
            public string Extension { get; set; }
        }

        public ActionResult NotFound()
        {
            return View();
        }
    }
}
