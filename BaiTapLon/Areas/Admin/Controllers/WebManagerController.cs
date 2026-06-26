using Mood.Draw;
using Mood.EF2;
using BaiTapLon.Services;
using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Globalization;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace BaiTapLon.Areas.Admin.Controllers
{
    public class WebManagerController : BaseController
    {
        // GET: Admin/WebManager
        public ActionResult Index()
        {
            return View();
        }

        [HttpGet]
        public ActionResult StoreLocation(int? id = null)
        {
            using (var db = new QuanLySachDBContext())
            {
                var model = id.HasValue
                    ? db.StoreLocations.AsNoTracking().SingleOrDefault(x => x.ID == id.Value)
                    : db.StoreLocations.AsNoTracking().OrderByDescending(x => x.IsActive).ThenBy(x => x.SortOrder).FirstOrDefault();

                if (model == null)
                {
                    model = new StoreLocationService().CreateDefaultStore();
                }

                ViewBag.Stores = db.StoreLocations.AsNoTracking().OrderBy(x => x.SortOrder).ThenBy(x => x.StoreName).ToList();
                return View(model);
            }
        }

        [HttpPost]
        [ValidateInput(false)]
        public ActionResult StoreLocation(StoreLocation model)
        {
            decimal parsedValue;
            if (TryReadDecimal("Latitude", out parsedValue))
            {
                model.Latitude = parsedValue;
                ModelState.Remove("Latitude");
            }

            if (TryReadDecimal("Longitude", out parsedValue))
            {
                model.Longitude = parsedValue;
                ModelState.Remove("Longitude");
            }

            if (TryReadDecimal("GeofenceRadius", out parsedValue))
            {
                model.GeofenceRadius = (double)parsedValue;
                ModelState.Remove("GeofenceRadius");
            }

            if (model.Latitude < -90 || model.Latitude > 90)
            {
                ModelState.AddModelError("Latitude", "Vĩ độ phải nằm trong khoảng -90 đến 90.");
            }

            if (model.Longitude < -180 || model.Longitude > 180)
            {
                ModelState.AddModelError("Longitude", "Kinh độ phải nằm trong khoảng -180 đến 180.");
            }

            if (model.GeofenceRadius <= 0)
            {
                ModelState.AddModelError("GeofenceRadius", "Bán kính phải lớn hơn 0.");
            }

            if (ModelState.IsValid)
            {
                using (var db = new QuanLySachDBContext())
                {
                    if (model.ID > 0)
                    {
                        if (model.IsActive)
                        {
                            var otherStores = db.StoreLocations.Where(x => x.ID != model.ID && x.IsActive).ToList();
                            foreach (var store in otherStores)
                            {
                                store.IsActive = false;
                            }
                        }

                        db.Entry(model).State = EntityState.Modified;
                    }
                    else
                    {
                        if (model.IsActive)
                        {
                            var activeStores = db.StoreLocations.Where(x => x.IsActive).ToList();
                            foreach (var store in activeStores)
                            {
                                store.IsActive = false;
                            }
                        }

                        db.StoreLocations.Add(model);
                    }

                    db.SaveChanges();
                    TempData["StoreLocationMessage"] = "Cập nhật thông tin nhà sách thành công.";
                    return RedirectToAction("StoreLocation", new { id = model.ID });
                }
            }

            using (var db = new QuanLySachDBContext())
            {
                ViewBag.Stores = db.StoreLocations.AsNoTracking().OrderBy(x => x.SortOrder).ThenBy(x => x.StoreName).ToList();
            }

            return View(model);
        }

        private bool TryReadDecimal(string fieldName, out decimal value)
        {
            value = 0;
            var rawValue = Request.Form[fieldName];
            if (string.IsNullOrWhiteSpace(rawValue))
            {
                return false;
            }

            rawValue = rawValue.Trim();
            return decimal.TryParse(rawValue, NumberStyles.Float, CultureInfo.InvariantCulture, out value)
                || decimal.TryParse(rawValue, NumberStyles.Float, CultureInfo.CurrentCulture, out value)
                || decimal.TryParse(rawValue.Replace(',', '.'), NumberStyles.Float, CultureInfo.InvariantCulture, out value);
        }

        public ActionResult Menu(string searhString, int page = 1, int pagesize = 5)
        {
            var modelMenu = new MenuDraw().listMenu(searhString, page, pagesize);
            return View(modelMenu);
        }
        [HttpGet]
        public ActionResult MenuCreate()
        {
            setViewBagMenu();
            return View();
        }

        [HttpPost]
        public ActionResult MenuCreate(Menu modelMenu, string Target2)
        {
            if (ModelState.IsValid)
            {
                var draw = new MenuDraw();
                if (!draw.checkNameMenu(modelMenu.NameMenu))
                {
                    modelMenu.CreateDate = DateTime.Now;
                    if (Target2.Equals("1"))
                    {
                        modelMenu.Target = "_blank";
                    }
                    else
                    {
                        modelMenu.Target = "_self";
                    }
                    var result = new MenuDraw().InsertMenu(modelMenu);
                    if (result > 0)
                    {
                        ModelState.AddModelError("menuSuccess", "Tạo mới menu thành công");
                    }
                    else
                    {
                        ModelState.AddModelError("menu", "Không thể tạo menu mới!!");
                    }
                }
                else
                {
                    ModelState.AddModelError("menu", "Tên menu đã tồn tại !!!");
                }
            }
            else
            {
                ModelState.AddModelError("menu", "Không thể tạo menu mới!!");
            }
            setViewBagMenu();
            return View("MenuCreate");
        }
        [HttpGet]
        public ActionResult MenuEdit(long id)
        {
            setViewBagMenu();
            var modelMenu = new MenuDraw().viewDetails(id);
            ViewBag.target = modelMenu.Target;
            return View(modelMenu);
        }
        [HttpPost]
        public ActionResult MenuEdit(Menu modelMenu, string Target2)
        {
            var model = new MenuDraw().viewDetails(modelMenu.IDMenu);
            ViewBag.target = model.Target;
            if (ModelState.IsValid)
            {
                var draw = new MenuDraw();

                modelMenu.CreateDate = DateTime.Now;
                if (Target2.Equals("1"))
                {
                    modelMenu.Target = "_blank";
                }
                else
                {
                    modelMenu.Target = "_self";
                }
                var result = new MenuDraw().UpdateMenu(modelMenu);

                if (result)
                {
                    ModelState.AddModelError("menuSuccess", "Cập nhật menu thành công");
                }
                else
                {
                    ModelState.AddModelError("menu", "Không thể cập nhật menu!!");
                    
                }
            }
            else
            {
                ModelState.AddModelError("menu", "Không thể cập nhật menu!!");
                
            }
            setViewBagMenu();
            return View("MenuEdit");
        }

        public void setViewBagMenu(long? selectedId = null)
        {
            var dao = new MenuDraw();
            ViewBag.MenuTypeID = new SelectList(dao.listAllMenuType(), "MenuTypeID", "NameType", selectedId);// bên trong chưa 3 tham số list, giá trị ID, tên hiển thị
        }
        [HttpDelete]
        public ActionResult Delete(long id)
        {
            new MenuDraw().Delete(id);
            return View();
        }
        public ActionResult Silder(string searhString, int page = 1, int pagesize = 5)
        {
            var modelSilder = new SildeDraw().listSilderView(searhString, page, pagesize);
            return View(modelSilder);
        }
        [HttpGet]
        public ActionResult SliderCreate()
        {
            return View();
        }

        [HttpPost]
        public ActionResult SliderCreate(Slide model)
        {
            if(ModelState.IsValid)
            {
                var draw = new SildeDraw();
                if(!draw.checkThuTu(model.DisPlayOrder))
                {
                    var result = new SildeDraw().InsertSlider(model);
                    if(result > 0)
                    {
                        ModelState.AddModelError("sliderSuccess", "Thêm mới slider thành công");
                    }else
                    {
                        ModelState.AddModelError("slider", "Không thể thêm mới slider!!!");
                    }
                }
                else
                {
                    ModelState.AddModelError("slider", "Thứ tự này đã có siler khác!!!");
                }
            }else
            {
                ModelState.AddModelError("slider", "Không thể thêm mới silder!!!");
            }
            return View("SliderCreate");
        }

        [HttpDelete]
        public ActionResult DeleteSlider(long id)
        {
            new SildeDraw().DeleteSlider(id);
            return View();
        }
        [HttpGet]
        public ActionResult SliderEdit(long id)
        {
            var modelSlider = new SildeDraw().viewDetails(id);
            return View(modelSlider);
        }
        [HttpPost]
        public ActionResult SliderEdit(Slide model)
        {
            if (ModelState.IsValid)
            {
                var draw = new SildeDraw();
                
                    var result = new SildeDraw().UpdateSilder(model);
                    if (result)
                    {
                        ModelState.AddModelError("sliderSuccess", "Cập nhật slider thành công");
                    }
                    else
                    {
                        ModelState.AddModelError("slider", "Không thể cập nhật slider!!!");
                    }
               
            }
            else
            {
                ModelState.AddModelError("slider", "Không thể cập nhật silder!!!");
            }
            return View("SliderEdit");
        }
    }
}
