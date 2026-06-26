using System.Net;
using System.Threading.Tasks;
using System.Web.Mvc;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace Tests
{
    [TestClass]
    public class FaceAuthControllerTests
    {
        [TestMethod]
        public async Task RegisterFace_NoFile_ReturnsBadRequest()
        {
            var controller = new BaiTapLon.Controllers.FaceAuthController();
            var result = await controller.RegisterFace(0) as HttpStatusCodeResult;
            Assert.IsNotNull(result);
            Assert.AreEqual((int)HttpStatusCode.BadRequest, result.StatusCode);
        }

        [TestMethod]
        public async Task VerifyFace_NoFile_ReturnsJson()
        {
            var controller = new BaiTapLon.Controllers.FaceAuthController();
            var result = await controller.VerifyFace(0) as JsonResult;
            Assert.IsNotNull(result);
            Assert.IsNotNull(result.Data);
        }
    }
}
