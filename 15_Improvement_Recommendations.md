# 15. Architectural & Security Improvement Recommendations

This document outlines structural, security, and performance improvements to modernize the application.

---

## 1. Security Improvements

### Replace MD5 Password Hashing
- **Issue**: Passwords are saved as MD5 hashes which are insecure.
- **Action**: Replace `EncryptorMD5` with a modern hashing library (like BCrypt.Net). Implement automatic migration of password hashes when users log in.

### Remove Hardcoded Credentials
- **Issue**: Fixed credentials (`admin` / `123456`) are checked directly in `UsersController.cs`.
- **Action**: Remove `IsFixedAdminLogin()` and `SignInFixedAdmin()`. Admin users should be stored in the database with strong, unique passwords.

### Encrypt Web.config Secrets
- **Issue**: SMTP passwords and Facebook secrets are stored in plain text.
- **Action**: Encrypt the configuration sections using `aspnet_regiis` or load them from secure environment variables.

---

## 2. Architectural & Code Quality Improvements

### Introduce Dependency Injection (DI) & Interfaces
- **Issue**: Controllers explicitly instantiate DAO classes (e.g., `var dao = new UserDraw();`), preventing unit testing and mock configurations.
- **Action**: Introduce interfaces for DAO repositories (e.g. `ISanphamRepository`) and inject them via constructor injection using a DI container (e.g., Autofac).

### Extract Business Workflows from Controllers
- **Issue**: Controllers are handling business logic such as inventory checks, file uploads, coordinate math, and email assembly.
- **Action**: Move business logic to separate service classes (e.g., `RentalService`, `UserService`), keeping controllers focused solely on handling web requests.

### Avoid Swallowing Exceptions
- **Issue**: Catch blocks inside `LogRepository.cs` are left empty:
  ```csharp
  catch {
      // Logging must not break the main user flow.
  }
  ```
- **Action**: Avoid empty catch blocks. Log exceptions using a structured logging framework (like NLog or Serilog) to a file or error tracking dashboard.

---

## 3. Performance Optimizations

### Transition to Async Database Queries
- **Issue**: Almost all database queries in `Mood.Draw` are synchronous, which blocks execution threads.
- **Action**: Update queries to use Entity Framework's async extensions (e.g., `ToListAsync()`, `SaveChangesAsync()`, `FirstOrDefaultAsync()`).

### Implement Caching for Static Master Data
- **Issue**: Store location data is loaded from the database for every geofence check.
- **Action**: Cache store locations in `HttpRuntime.Cache` and invalidate the cache only when an administrator updates store details in the dashboard.
