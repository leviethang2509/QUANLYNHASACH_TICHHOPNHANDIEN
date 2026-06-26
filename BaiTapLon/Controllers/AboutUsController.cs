using BaiTapLon.Services;
using System.Web.Mvc;

namespace BaiTapLon.Controllers
{
    public class AboutUsController : Controller
    {
        public ActionResult Index()
        {
            var store = new StoreLocationService().GetActiveStore();
            return View(store);
        }
    }
}
