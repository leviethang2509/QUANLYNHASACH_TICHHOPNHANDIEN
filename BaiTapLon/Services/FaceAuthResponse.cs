namespace BaiTapLon.Services
{
    public class FaceAuthResponse
    {
        public bool Success { get; set; }
        public double Confidence { get; set; }
        public string UserId { get; set; }
        public string ExternalUserId { get; set; }
        public bool LivenessPassed { get; set; }
        public string ErrorCode { get; set; }
        public string ErrorMessage { get; set; }
        public string RequestId { get; set; }
        public string Purpose { get; set; }
        public string Error { get; set; }
        public bool ActionMatched { get; set; }
        public string ActionCode { get; set; }
        public string ActionMessage { get; set; }
    }
}
