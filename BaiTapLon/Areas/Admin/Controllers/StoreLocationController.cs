using Mood.EF2;
using System.Linq;
using System.Web.Mvc;

namespace BaiTapLon.Areas.Admin.Controllers
{
    [Authorize(Roles = "Admin")]
    public class StoreLocationController : Controller
    {
        private readonly LogDbContext _db = new LogDbContext();

        public ActionResult Index()
        {
            var stores = _db.Set<StoreLocation>().ToList();
            return View(stores);
        }

        public ActionResult Create() => View();

        [HttpPost]
        public ActionResult Create(StoreLocation model)
        {
            if (!ModelState.IsValid) return View(model);
            _db.Set<StoreLocation>().Add(model);
            _db.SaveChanges();
            return RedirectToAction("Index");
        }

        public ActionResult Edit(int id)
        {
            var m = _db.Set<StoreLocation>().Find(id);
            return View(m);
        }

        [HttpPost]
        public ActionResult Edit(StoreLocation model)
        {
            if (!ModelState.IsValid) return View(model);
            _db.Entry(model).State = System.Data.Entity.EntityState.Modified;
            _db.SaveChanges();
            return RedirectToAction("Index");
        }

        public ActionResult Delete(int id)
        {
            var m = _db.Set<StoreLocation>().Find(id);
            if (m != null) { _db.Set<StoreLocation>().Remove(m); _db.SaveChanges(); }
            return RedirectToAction("Index");
        }
    }
}
