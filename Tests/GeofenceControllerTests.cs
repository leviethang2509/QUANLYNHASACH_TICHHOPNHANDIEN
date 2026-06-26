using System.Web.Mvc;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace Tests
{
    [TestClass]
    public class GeofenceControllerTests
    {
        [TestMethod]
        public void CheckGeofence_InvalidLatitude_ReturnsJsonError()
        {
            var controller = new BaiTapLon.Controllers.GeofenceController();

            var result = controller.CheckGeofence(100, 106, 1) as JsonResult;

            Assert.IsNotNull(result);
            Assert.IsNotNull(result.Data);
        }
    }
}
