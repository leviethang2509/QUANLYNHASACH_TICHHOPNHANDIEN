# 12. Security Review

This document assesses the security posture of the bookstore system, highlighting strengths, vulnerabilities, and remediation recommendations.

---

## 1. Security Strengths
- **SQL Injection Mitigation**: Data access is managed by Entity Framework 6. System operations use parameterized LINQ expressions, preventing raw string concatenation issues. Raw SQL calls inside `LogRepository.cs` use static SQL strings, preventing SQL Injection risks.
- **XSS Mitigation**: The presentation layer utilizes ASP.NET MVC Razor view templates. Razor naturally encodes output variables before rendering, mitigating reflection Cross-Site Scripting (XSS).
- **CAPTCHA Validation**: Integrated BotDetect CAPTCHA checks in user-facing submission views prevent brute-force login attempts and automated spam registrations.

---

## 2. Key Security Risks & Vulnerabilities

### Cryptographically Broken Hashing Algorithm (MD5)
- **Finding**: User passwords are saved using MD5 hashes (`EncryptorMD5.GetMD5`).
- **Risk**: MD5 is highly vulnerable to dictionary lookup tables, pre-computation attacks, and collision generation. A database leak would compromise all user passwords.
- **Remediation**: Transition to a secure algorithm like **BCrypt**, **PBKDF2**, or **Argon2** with unique salting.

### Plain Text Configuration Secrets
- **Finding**: Plain text secrets (e.g. SMTP passwords, Facebook APP secrets) are stored directly inside `Web.config`:
  - `<add key="FromEmailPassword" value="uwiw rhpu imtf jhcu"/>`
  - `<add key="FBAppSecret" value="068493c72412be74cd841f98ba5cc7e0"/>`
- **Risk**: Storing passwords in configuration files risks exposure via source control or configuration leaks.
- **Remediation**: Use environment variables or encrypt the `connectionStrings` and `appSettings` sections of the `Web.config` using ASP.NET IIS registration tools.

### Weak Admin Fallback Credentials
- **Finding**: `IsFixedAdminLogin()` checks for hardcoded credentials: username `admin` and password `123456`.
- **Risk**: An attacker could log in as administrator using this simple password.
- **Remediation**: Delete hardcoded credentials. Admin credentials should be managed inside the database with strong password policies.

### Lack of HTTPS Enforcement
- **Finding**: While `MvcApplication` redirects absolute HTTP redirect calls (`Application_BeginRequest` in `Global.asax.cs`), there are no explicit `[RequireHttps]` attributes enforced on login/registration forms or checkout controllers.
- **Risk**: Session cookies (`ASP.NET_SessionId`) could be intercepted over unencrypted channels.
- **Remediation**: Enforce SSL redirect policies in IIS and mark session cookies as `HttpOnly` and `Secure`.
