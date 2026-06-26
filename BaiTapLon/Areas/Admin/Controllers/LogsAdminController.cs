using BaiTapLon.Areas.Admin.Models;
using Common.Repositories;
using Mood.EF2;
using System;
using System.Collections.Generic;
using System.Web.Mvc;

namespace BaiTapLon.Areas.Admin.Controllers
{
    public class LogsAdminController : BaseController
    {
        private readonly LogRepository _logRepo = new LogRepository();

        public ActionResult FaceAuth(int page = 1, int pageSize = 50, long? userId = null, string action = null, DateTime? fromDate = null, DateTime? toDate = null, bool? result = null)
        {
            var logs = _logRepo.GetFaceAuthLogs(page, pageSize, userId, action, fromDate, toDate, result);
            ViewBag.RuntimeDatabase = _logRepo.GetRuntimeDatabaseInfo();
            ViewBag.AllCount = _logRepo.GetFaceAuthLogs(1, 1).Total;
            var todayLogs = _logRepo.GetFaceAuthLogs(1, 1, null, null, DateTime.Today, DateTime.Today.AddDays(1), null);
            var successLogs = _logRepo.GetFaceAuthLogs(1, 1, userId, action, fromDate, toDate, true);
            var failedLogs = _logRepo.GetFaceAuthLogs(1, 1, userId, action, fromDate, toDate, false);
            ViewBag.SuccessCount = successLogs.Total;
            ViewBag.FailedCount = failedLogs.Total;
            ViewBag.TodayCount = todayLogs.Total;
            return View("~/Areas/Admin/Views/Logs/FaceAuthLogs.cshtml", new LogFilterModel<IList<FaceAuthLog>>
            {
                Logs = logs.Items,
                Total = logs.Total,
                Page = logs.Page,
                PageSize = logs.PageSize,
                UserId = userId,
                Action = action,
                FromDate = fromDate,
                ToDate = toDate,
                Result = result
            });
        }

        public ActionResult Geofence(int page = 1, int pageSize = 50, long? userId = null, int? storeId = null, DateTime? fromDate = null, DateTime? toDate = null, bool? inZone = null)
        {
            var logs = _logRepo.GetGeofenceLogs(page, pageSize, userId, storeId, fromDate, toDate, inZone);
            ViewBag.RuntimeDatabase = _logRepo.GetRuntimeDatabaseInfo();
            ViewBag.AllCount = _logRepo.GetGeofenceLogs(1, 1).Total;
            var todayLogs = _logRepo.GetGeofenceLogs(1, 1, null, null, DateTime.Today, DateTime.Today.AddDays(1), null);
            var inZoneLogs = _logRepo.GetGeofenceLogs(1, 1, userId, storeId, fromDate, toDate, true);
            var outZoneLogs = _logRepo.GetGeofenceLogs(1, 1, userId, storeId, fromDate, toDate, false);
            ViewBag.InZoneCount = inZoneLogs.Total;
            ViewBag.OutZoneCount = outZoneLogs.Total;
            ViewBag.TodayCount = todayLogs.Total;
            return View("~/Areas/Admin/Views/Logs/GeofenceLogs.cshtml", new LogFilterModel<IList<GeofenceLog>>
            {
                Logs = logs.Items,
                Total = logs.Total,
                Page = logs.Page,
                PageSize = logs.PageSize,
                UserId = userId,
                StoreId = storeId,
                FromDate = fromDate,
                ToDate = toDate,
                InZone = inZone
            });
        }

        public ActionResult Rental(int page = 1, int pageSize = 50, long? userId = null, int? rentalId = null, string action = null, DateTime? fromDate = null, DateTime? toDate = null)
        {
            var logs = _logRepo.GetRentalLogs(page, pageSize, userId, rentalId, action, fromDate, toDate);
            ViewBag.RuntimeDatabase = _logRepo.GetRuntimeDatabaseInfo();
            ViewBag.AllCount = _logRepo.GetRentalLogs(1, 1).Total;
            ViewBag.RequestCount = _logRepo.GetRentalLogs(1, 1, userId, rentalId, "Request", fromDate, toDate).Total;
            ViewBag.ApproveCount = _logRepo.GetRentalLogs(1, 1, userId, rentalId, "Approve", fromDate, toDate).Total
                + _logRepo.GetRentalLogs(1, 1, userId, rentalId, "Borrow", fromDate, toDate).Total;
            ViewBag.ReturnCount = _logRepo.GetRentalLogs(1, 1, userId, rentalId, "Return", fromDate, toDate).Total;
            ViewBag.OverdueCount = _logRepo.GetRentalLogs(1, 1, userId, rentalId, "Overdue", fromDate, toDate).Total;
            return View("~/Areas/Admin/Views/Logs/RentalLogs.cshtml", new LogFilterModel<IList<RentalLog>>
            {
                Logs = logs.Items,
                Total = logs.Total,
                Page = logs.Page,
                PageSize = logs.PageSize,
                UserId = userId,
                RentalId = rentalId,
                Action = action,
                FromDate = fromDate,
                ToDate = toDate
            });
        }
    }
}

