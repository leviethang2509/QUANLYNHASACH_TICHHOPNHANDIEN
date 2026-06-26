using System.Web.Mvc;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace Tests
{
    [TestClass]
    public class RentalControllerTests
    {
        [TestMethod]
        public void RequestRental_AnonymousUser_ReturnsJsonError()
        {
            var controller = new BaiTapLon.Controllers.RentalController();

            var result = controller.RequestRental(1) as JsonResult;

            Assert.IsNotNull(result);
            Assert.IsNotNull(result.Data);
        }

        [TestMethod]
        public void UpdateRentalStatus_InvalidStatus_ReturnsJsonError()
        {
            var controller = new BaiTapLon.Controllers.RentalController();

            var result = controller.UpdateRentalStatus(1, "Invalid", 1) as JsonResult;

            Assert.IsNotNull(result);
            Assert.IsNotNull(result.Data);
        }
    }
}
