using Common.Repositories;
using System;
using System.Web.Mvc;

namespace BaiTapLon.Controllers.Api
{
    [Authorize(Roles = "Admin")]
    public class LogsController : Controller
    {
        private readonly LogRepository _logRepo = new LogRepository();

        public JsonResult Face(int page = 1, int pageSize = 50, long? userId = null, string action = null, DateTime? fromDate = null, DateTime? toDate = null, bool? result = null)
        {
            var logs = _logRepo.GetFaceAuthLogs(page, pageSize, userId, action, fromDate, toDate, result);
            return Json(logs, JsonRequestBehavior.AllowGet);
        }

        public JsonResult Geofence(int page = 1, int pageSize = 50, long? userId = null, int? storeId = null, DateTime? fromDate = null, DateTime? toDate = null, bool? inZone = null)
        {
            var logs = _logRepo.GetGeofenceLogs(page, pageSize, userId, storeId, fromDate, toDate, inZone);
            return Json(logs, JsonRequestBehavior.AllowGet);
        }

        public JsonResult Rental(int page = 1, int pageSize = 50, long? userId = null, int? rentalId = null, string action = null, DateTime? fromDate = null, DateTime? toDate = null)
        {
            var logs = _logRepo.GetRentalLogs(page, pageSize, userId, rentalId, action, fromDate, toDate);
            return Json(logs, JsonRequestBehavior.AllowGet);
        }
    }
}
