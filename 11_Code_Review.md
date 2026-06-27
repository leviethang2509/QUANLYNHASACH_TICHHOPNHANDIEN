# 11. Code Quality & Design Review

This document evaluates the codebase's architecture quality against standard software design principles (SOLID, DRY, KISS).

---

## 1. SOLID Principles Evaluation

### Single Responsibility Principle (SRP)
- **Strengths**: The system splits responsibilities into projects: `CommomSentMail` handles mailing, `Common` coordinates logging, and `Mood` stores entities and DAOs.
- **Weaknesses**: Controllers (especially `FaceAuthController.cs` and `RentalController.cs`) are very large and handle multiple concerns: filesystem uploads, parsing JSON payloads, validating coordinate bounds, sending email templates, and database coordination. These should be extracted into separate business services.

### Open/Closed Principle (OCP)
- **Weaknesses**: Adding new notification paths (e.g., SMS, push notifications) or database logging stores requires editing the core code of controllers or repositories directly. There are no abstractions or event-driven patterns in place.

### Liskov Substitution Principle (LSP)
- **Adherence**: Controllers inherit standard properties from `System.Web.Mvc.Controller` and `BaseController` without overriding base class definitions in a way that breaks behavior.

### Interface Segregation Principle (ISP)
- **Evaluation**: The project uses concrete classes for database queries and HTTP communications. There are very few custom interfaces defined in the solution, making this principle moot in practice.

### Dependency Inversion Principle (DIP)
- **Violations**: High-level modules (Controllers) directly instantiate concrete lower-level modules (DAOs, services):
  - `private readonly LogRepository _logRepo = new LogRepository();`
  - `var dao = new UserDraw();`
  - This prevents developers from writing unit tests with mock behaviors, as database actions are hardcoded.

---

## 2. DRY & KISS Principles

### DRY (Don't Repeat Yourself)
- **Code Duplication**: Utility functions are copied across different controller files:
  - `ReadString()`, `ReadDouble()`, and `ParseDate()` are duplicated in both `FaceAuthController.cs` and `RentalController.cs`.
  - Coordinate parsing and parsing exceptions are duplicated between `GeofenceController.cs` and `RentalController.cs`.
  - These should be consolidated into a shared helper class (e.g., `JsonParserHelper.cs` or `CoordinatesHelper.cs`).

### KISS (Keep It Simple, Stupid)
- **Adherence**: The query logic in DAO files is simple. Direct LINQ joins or plain queries make the database actions easy to understand for junior developers.

---

## 3. Code Maintainability & Suggestions

| Finding / Issue | Severity | Recommendation |
| :--- | :--- | :--- |
| Concrete Tight Coupling | Medium | Introduce interfaces (e.g., `IUserRepository`, `IBookService`) and set up a Dependency Injection container (Autofac or Microsoft.Extensions.DependencyInjection) in `Startup.cs`. |
| Duplicated JSON Parsers | Low | Move parsing helpers out of controllers and place them inside a shared utilities folder in the `Common` project. |
| Mixed Business Logic in Controllers | Medium | Move stock-level updates and check-out workflows from `RentalController` to a dedicated `BookRentalService`. |
