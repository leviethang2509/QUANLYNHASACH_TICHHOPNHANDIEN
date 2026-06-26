using System.Web.Mvc;

namespace BaiTapLon.Controllers
{
    public class HealthController : Controller
    {
        public ActionResult Ping() => Content("OK");

        public ActionResult FaceApi() 
        {
            var api = System.Configuration.ConfigurationManager.AppSettings["FaceAuthAPI"];
            if (string.IsNullOrEmpty(api)) return new HttpStatusCodeResult(500, "Face API not configured");
            return Content("OK");
        }
    }
}
