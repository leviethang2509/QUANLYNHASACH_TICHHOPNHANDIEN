# 09. Design Patterns

This document identifies and describes the design patterns implemented throughout the codebase, citing exact implementation classes.

---

## 1. Model-View-Controller (MVC) Pattern
- **Implementation**: Enforced by the ASP.NET MVC framework inside the `BaiTapLon` project.
- **Components**:
  - **Models**: Binds client data (e.g., `RegisterModel` inside `BaiTapLon/Models/RegisterModel.cs`).
  - **Views**: Razor templates located under `BaiTapLon/Views/` rendering layout templates and visual controls.
  - **Controllers**: Classes inheriting from `System.Web.Mvc.Controller` (e.g., `RentalController` in `BaiTapLon/Controllers/RentalController.cs`) orchestrating inputs and response generation.

---

## 2. Repository Pattern (DAO Variant)
- **Implementation**: Structured as Data Access Objects (DAOs) inside the `Mood.Draw` namespace.
- **Components**:
  - `UserDraw.cs` coordinates queries, insertions, status updates, and login validation code for users.
  - `SanphamDraw.cs` manages CRUD functions, remaining stock updates, and hot item settings.
  - `OrderDraw.cs` manages sales transactions database records.
- **Purpose**: Prevents raw database access statements or LINQ filters from leaking directly into Razor layouts or Controller bodies.

---

## 3. Gateway / Facade Pattern
- **Implementation**: Implemented by `FaceAuthApiClient.cs` inside `BaiTapLon.Services`.
- **Purpose**: Simplifies interactions with the external Flask server. Instead of forcing controllers to configure HttpClient instances, set headers, and build multipart form contents, they invoke simple methods:
  - `RegisterAsync()`
  - `VerifyAsync()`
  - `CheckActionAsync()`
  - `OcrIdentityCardAsync()`

---

## 4. Session State & Cache Token Guard Pattern
- **Implementation**: `FaceRentalTokenService.cs` inside `BaiTapLon.Services`.
- **Purpose**: Ensures book rentals are validated sequentially. Upon passing GPS proximity and webcam liveness challenge verification, the system issues a volatile GUID token, caching it in `HttpRuntime.Cache`. The checkout endpoint validates and consumes the token to complete the transaction.

---

## 5. Architectural Style Observations & Limitations
- **No Dependency Injection Container**: The system does not use DI containers (e.g., Autofac, Ninject) or constructor injection. Instead, it relies on manual dependency instantiation:
  - `private readonly LogRepository _logRepo = new LogRepository();`
  - `var dao = new UserDraw();`
- **Tight Coupling**: Controllers are tightly coupled to specific DAO class implementations, which affects unit test mockability.
- **Unit of Work**: The Entity Framework `DbContext` serves as the implicit Unit of Work, keeping track of changes and committing them atomically via `db.SaveChanges()`.
