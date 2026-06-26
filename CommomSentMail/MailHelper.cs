using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Configuration;
using System.Net.Mail;
using System.Net;

namespace CommomSentMail
{
    public class MailHelper
    {
        public void sentMail(string toEmailAddress,string subject,string content)
        {
            var fromEmailAddress = ConfigurationManager.AppSettings["FromEmailAddress"].ToString();

            var fromEmailDisplayName = "";
            if (subject.Equals("Yêu cầu thay đổi mật khẩu"))
            {
                fromEmailDisplayName = "Yêu cầu thay đổi mật khẩu";
            }
            else
            {
                fromEmailDisplayName = ConfigurationManager.AppSettings["FromEmailDisplayName"].ToString();
            }
            var fromEmailPassword = ConfigurationManager.AppSettings["FromEmailPassword"].ToString();
            if (!string.IsNullOrWhiteSpace(fromEmailPassword))
            {
                fromEmailPassword = fromEmailPassword.Replace(" ", string.Empty);
            }
            var smtpHost = ConfigurationManager.AppSettings["SMTPHost"].ToString();
            var smtpPort = ConfigurationManager.AppSettings["SMTPPort"].ToString();

            bool enabledSsl = bool.Parse(ConfigurationManager.AppSettings["EnabledSSL"].ToString());
            string body = content;
            ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;

            using (MailMessage message = new MailMessage(new MailAddress(fromEmailAddress, fromEmailDisplayName), new MailAddress(toEmailAddress)))
            using (var client = new SmtpClient())
            {
                message.Subject = subject;
                message.IsBodyHtml = true;
                message.Body = body;

                client.Host = smtpHost;
                client.Port = !string.IsNullOrEmpty(smtpPort) ? Convert.ToInt32(smtpPort) : 0;
                client.DeliveryMethod = SmtpDeliveryMethod.Network;
                client.UseDefaultCredentials = false;
                client.EnableSsl = enabledSsl;
                client.Credentials = new NetworkCredential(fromEmailAddress, fromEmailPassword);
                client.Send(message);
            }
        }
    }
}
