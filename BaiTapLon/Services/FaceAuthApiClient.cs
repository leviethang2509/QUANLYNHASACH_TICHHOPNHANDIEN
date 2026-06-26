using Newtonsoft.Json.Linq;
using System;
using System.Configuration;
using System.Globalization;
using System.IO;
using System.Net.Http;
using System.Threading.Tasks;

namespace BaiTapLon.Services
{
    public class FaceAuthApiClient
    {
        public async Task<FaceAuthResponse> RegisterAsync(string imagePath, string fileName, long userId)
        {
            return await PostFaceAsync("register", imagePath, fileName, userId, "Register");
        }

        public async Task<FaceAuthResponse> VerifyAsync(string imagePath, string fileName, long userId)
        {
            return await PostFaceAsync("verify", imagePath, fileName, userId, "Verify");
        }

        public async Task<FaceAuthResponse> VerifyAsync(string imagePath, string fileName, long userId, string purpose)
        {
            return await PostFaceAsync("verify", imagePath, fileName, userId, purpose);
        }

        public async Task<FaceAuthResponse> AuthenticateAsync(string imagePath, string fileName, long userId)
        {
            return await PostFaceAsync("authenticate", imagePath, fileName, userId, "MFA");
        }

        public async Task<FaceAuthResponse> CheckActionAsync(string imagePath, string fileName, long userId, string purpose, string actionCode)
        {
            return await PostFaceAsync("action-check", imagePath, fileName, userId, purpose, actionCode);
        }

        public async Task<JObject> OcrIdentityCardAsync(string imagePath, string fileName, long userId)
        {
            return await PostRawAsync("ocr-cmnd", imagePath, fileName, userId, "IdentityCard");
        }

        public async Task<JObject> OcrIdentityCardAsync(string frontImagePath, string frontFileName, string backImagePath, string backFileName, long userId, string purpose)
        {
            return await PostIdentityRawAsync("ocr-cmnd", frontImagePath, frontFileName, backImagePath, backFileName, userId, purpose ?? "IdentityCard");
        }

        private async Task<JObject> PostIdentityRawAsync(string endpoint, string frontImagePath, string frontFileName, string backImagePath, string backFileName, long userId, string purpose)
        {
            var baseUrl = (ConfigurationManager.AppSettings["FaceAuthAPI"] ?? string.Empty).TrimEnd('/');
            if (string.IsNullOrWhiteSpace(baseUrl))
            {
                return JObject.FromObject(new { success = false, error_code = "CONFIG_MISSING", error_message = "FaceAuthAPI is not configured" });
            }

            try
            {
                using (var client = new HttpClient())
                using (var content = new MultipartFormDataContent())
                {
                    client.Timeout = TimeSpan.FromSeconds(GetTimeoutSeconds());
                    StreamContent frontContent = null;
                    StreamContent backContent = null;
                    FileStream frontStream = null;
                    FileStream backStream = null;

                    try
                    {
                        if (!string.IsNullOrWhiteSpace(frontImagePath) && File.Exists(frontImagePath))
                        {
                            frontStream = File.OpenRead(frontImagePath);
                            frontContent = new StreamContent(frontStream);
                            content.Add(frontContent, "front_file", frontFileName);
                        }

                        if (!string.IsNullOrWhiteSpace(backImagePath) && File.Exists(backImagePath))
                        {
                            backStream = File.OpenRead(backImagePath);
                            backContent = new StreamContent(backStream);
                            content.Add(backContent, "back_file", backFileName);
                        }

                        if (frontContent == null && backContent == null)
                        {
                            return JObject.FromObject(new { success = false, error_code = "NO_FILE", error_message = "Identity image is required" });
                        }

                        content.Add(new StringContent(userId.ToString()), "userId");
                        content.Add(new StringContent(userId.ToString()), "user_id");
                        content.Add(new StringContent(purpose ?? string.Empty), "purpose");

                        var response = await client.PostAsync(baseUrl + "/" + endpoint, content);
                        var body = await response.Content.ReadAsStringAsync();
                        if (!response.IsSuccessStatusCode)
                        {
                            return JObject.FromObject(new { success = false, error_code = "HTTP_" + (int)response.StatusCode, error_message = response.StatusCode + ": " + body });
                        }

                        return JObject.Parse(body);
                    }
                    finally
                    {
                        if (frontStream != null) frontStream.Dispose();
                        if (backStream != null) backStream.Dispose();
                    }
                }
            }
            catch (Exception ex)
            {
                return JObject.FromObject(new { success = false, error_code = "CLIENT_EXCEPTION", error_message = ex.Message });
            }
        }

        private async Task<JObject> PostRawAsync(string endpoint, string imagePath, string fileName, long userId, string purpose)
        {
            var baseUrl = (ConfigurationManager.AppSettings["FaceAuthAPI"] ?? string.Empty).TrimEnd('/');
            if (string.IsNullOrWhiteSpace(baseUrl))
            {
                return JObject.FromObject(new { success = false, error_code = "CONFIG_MISSING", error_message = "FaceAuthAPI is not configured" });
            }

            try
            {
                using (var client = new HttpClient())
                using (var content = new MultipartFormDataContent())
                using (var fs = File.OpenRead(imagePath))
                {
                    client.Timeout = TimeSpan.FromSeconds(GetTimeoutSeconds());
                    content.Add(new StreamContent(fs), "file", fileName);
                    content.Add(new StringContent(userId.ToString()), "userId");
                    content.Add(new StringContent(userId.ToString()), "user_id");
                    content.Add(new StringContent(purpose ?? string.Empty), "purpose");

                    var response = await client.PostAsync(baseUrl + "/" + endpoint, content);
                    var body = await response.Content.ReadAsStringAsync();
                    if (!response.IsSuccessStatusCode)
                    {
                        return JObject.FromObject(new { success = false, error_code = "HTTP_" + (int)response.StatusCode, error_message = response.StatusCode + ": " + body });
                    }

                    return JObject.Parse(body);
                }
            }
            catch (Exception ex)
            {
                return JObject.FromObject(new { success = false, error_code = "CLIENT_EXCEPTION", error_message = ex.Message });
            }
        }

        private async Task<FaceAuthResponse> PostFaceAsync(string endpoint, string imagePath, string fileName, long userId, string purpose)
        {
            return await PostFaceAsync(endpoint, imagePath, fileName, userId, purpose, null);
        }

        private async Task<FaceAuthResponse> PostFaceAsync(string endpoint, string imagePath, string fileName, long userId, string purpose, string actionCode)
        {
            var baseUrl = (ConfigurationManager.AppSettings["FaceAuthAPI"] ?? string.Empty).TrimEnd('/');
            if (string.IsNullOrWhiteSpace(baseUrl))
            {
                return CreateErrorResponse("CONFIG_MISSING", "FaceAuthAPI is not configured", purpose);
            }

            try
            {
                using (var client = new HttpClient())
                using (var content = new MultipartFormDataContent())
                using (var fs = File.OpenRead(imagePath))
                {
                    client.Timeout = TimeSpan.FromSeconds(GetTimeoutSeconds());
                    content.Add(new StreamContent(fs), "file", fileName);
                    content.Add(new StringContent(userId.ToString()), "userId");
                    content.Add(new StringContent(userId.ToString()), "user_id");
                    content.Add(new StringContent(purpose ?? string.Empty), "purpose");
                    if (!string.IsNullOrWhiteSpace(actionCode))
                    {
                        content.Add(new StringContent(actionCode), "actionCode");
                        content.Add(new StringContent(actionCode), "action_code");
                    }

                    var response = await client.PostAsync(baseUrl + "/" + endpoint, content);
                    var body = await response.Content.ReadAsStringAsync();
                    if (!response.IsSuccessStatusCode)
                    {
                        return CreateErrorResponse("HTTP_" + (int)response.StatusCode, response.StatusCode + ": " + body, purpose);
                    }

                    var json = JObject.Parse(body);
                    var errorMessage = ReadString(json, "error", "message", "error_message");
                    return new FaceAuthResponse
                    {
                        Success = ReadBool(json, "success", "matched"),
                        Confidence = ReadDouble(json, "confidence", "quality_score"),
                        UserId = ReadString(json, "userId", "user_id"),
                        ExternalUserId = ReadString(json, "externalUserId", "external_user_id", "face_id"),
                        LivenessPassed = ReadBool(json, "livenessPassed", "liveness_passed"),
                        ErrorCode = ReadString(json, "errorCode", "error_code"),
                        ErrorMessage = errorMessage,
                        Error = errorMessage,
                        RequestId = ReadString(json, "requestId", "request_id"),
                        Purpose = ReadString(json, "purpose") ?? purpose,
                        ActionMatched = ReadBool(json, "actionMatched", "action_matched", "matched"),
                        ActionCode = ReadString(json, "actionCode", "action_code") ?? actionCode,
                        ActionMessage = ReadString(json, "actionMessage", "action_message")
                    };
                }
            }
            catch (Exception ex)
            {
                return CreateErrorResponse("CLIENT_EXCEPTION", ex.Message, purpose);
            }
        }

        private static FaceAuthResponse CreateErrorResponse(string errorCode, string errorMessage, string purpose)
        {
            return new FaceAuthResponse
            {
                Success = false,
                ErrorCode = errorCode,
                ErrorMessage = errorMessage,
                Error = errorMessage,
                Purpose = purpose
            };
        }

        private static string ReadString(JObject json, params string[] names)
        {
            foreach (var name in names)
            {
                var token = json[name];
                if (token != null && token.Type != JTokenType.Null)
                {
                    return token.Value<string>();
                }
            }

            return null;
        }

        private static bool ReadBool(JObject json, params string[] names)
        {
            foreach (var name in names)
            {
                var token = json[name];
                if (token != null && token.Type != JTokenType.Null)
                {
                    bool value;
                    if (bool.TryParse(token.ToString(), out value)) return value;
                }
            }

            return false;
        }

        private static double ReadDouble(JObject json, params string[] names)
        {
            foreach (var name in names)
            {
                var token = json[name];
                if (token != null && token.Type != JTokenType.Null)
                {
                    double value;
                    if (double.TryParse(token.ToString(), NumberStyles.Float, CultureInfo.InvariantCulture, out value)) return value;
                    if (double.TryParse(token.ToString(), out value)) return value;
                }
            }

            return 0.0;
        }

        private static int GetTimeoutSeconds()
        {
            int value;
            return int.TryParse(ConfigurationManager.AppSettings["FaceAuthTimeoutSeconds"], out value) && value > 0 ? value : 15;
        }
    }
}
