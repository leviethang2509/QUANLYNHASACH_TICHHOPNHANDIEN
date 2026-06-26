using System.Web.Mvc;
using System.Web.Routing;

namespace BaiTapLon
{
    public class RouteConfig
    {
        public static void RegisterRoutes(RouteCollection routes)
        {
            routes.IgnoreRoute("{resource}.axd/{*pathInfo}");

            routes.MapRoute(
                name: "DangNhap",
                url: "dang-nhap",
                defaults: new { controller = "Users", action = "DangNhap" }
            );

            routes.MapRoute(
                name: "ChiTietSanPham",
                url: "chi-tiet/{slug}-{idDetail}",
                defaults: new { controller = "Product", action = "Detail", slug = UrlParameter.Optional },
                constraints: new { idDetail = @"\d+" }
            );

            routes.MapRoute(
                name: "TongQuanTaiKhoan",
                url: "tong-quan-{id}",
                defaults: new { controller = "Users", action = "Dashboard" },
                constraints: new { id = @"\d+" }
            );

            routes.MapRoute(
                name: "ThongTinCaNhan",
                url: "thong-tin-ca-nhan-{id}",
                defaults: new { controller = "Users", action = "ProfileUser" },
                constraints: new { id = @"\d+" }
            );

            routes.MapRoute(
                name: "DanhSachDonHang",
                url: "danh-sach-don-hang-{id}",
                defaults: new { controller = "Users", action = "DanhSachHang" },
                constraints: new { id = @"\d+" }
            );

            routes.MapRoute(
                name: "TinNhanTaiKhoan",
                url: "tin-nhan-{id}",
                defaults: new { controller = "Users", action = "MessengerUser" },
                constraints: new { id = @"\d+" }
            );

            routes.MapRoute(
                name: "PhanHoiTaiKhoan",
                url: "phan-hoi-{id}",
                defaults: new { controller = "Users", action = "MessengerReply" },
                constraints: new { id = @"\d+" }
            );

            routes.MapRoute(
                name: "YeuThichTaiKhoan",
                url: "yeu-thich-{id}",
                defaults: new { controller = "Users", action = "Favorites" },
                constraints: new { id = @"\d+" }
            );

            routes.MapRoute(
                name: "YeuThichCucBo",
                url: "yeu-thich",
                defaults: new { controller = "Users", action = "Favorites" }
            );

            routes.MapRoute(
                name: "Default",
                url: "{controller}/{action}/{id}",
                defaults: new { controller = "Home", action = "TrangChu", id = UrlParameter.Optional }
            );
        }
    }
}
