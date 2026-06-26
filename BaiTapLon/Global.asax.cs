using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System;
using System.Web.Mvc;
using System.Web.Optimization;
using System.Web.Routing;

namespace BaiTapLon
{
    public class MvcApplication : System.Web.HttpApplication
    {
        protected void Application_BeginRequest()
        {
            var path = Request.Url.AbsolutePath;
            if (path.StartsWith("/http:", StringComparison.OrdinalIgnoreCase) ||
                path.StartsWith("/https:", StringComparison.OrdinalIgnoreCase))
            {
                Response.Redirect("~/", true);
            }
        }

        protected void Application_Start()
        {
            AreaRegistration.RegisterAllAreas();
            FilterConfig.RegisterGlobalFilters(GlobalFilters.Filters);
            RouteConfig.RegisterRoutes(RouteTable.Routes);
            BundleConfig.RegisterBundles(BundleTable.Bundles);
        }
    }
}
