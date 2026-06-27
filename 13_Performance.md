# 13. Performance Review

This document reviews system execution parameters, database query efficiency, asynchronous thread usages, and caching strategies.

---

## 1. Database Query Analysis & N+1 Prevention
- **Flat Projections**: The system avoids standard N+1 issues by query joining tables explicitly within LINQ blocks. For example, `ListViewUser` in `UserDraw.cs` joins `Users` and `Quyens` explicitly, returning a projected ViewModel:
  ```csharp
  from a in db.Users
  join b in db.Quyens on a.IDQuyen equals b.IDQuyen
  select new UserModelView() { ... }
  ```
- **Paginated Queries**: Pagination is implemented using `X.PagedList` (e.g., `ToPagedList(page, pageSize)`). This executes a `COUNT` query followed by a `SKIP / TAKE` select block on SQL Server, preventing out-of-memory errors by fetching only page-sized chunks.

---

## 2. Asynchronous Thread Execution (Async/Await)
- **Outer Requests**: Remote calls to the external Python Flask API are executed asynchronously (`async` / `await` pattern in `FaceAuthController.cs` and `FaceAuthApiClient.cs`). This releases ASP.NET thread pool threads during socket wait times, preventing thread starvation during slow OCR processing.
- **Database Access**: Almost all database transactions inside the DAO repository layer (`Mood/Draw`) are executed synchronously:
  - `db.SaveChanges();`
  - `db.Sanphams.Find(id);`
  - Under heavy traffic, synchronous database queries block execution threads, increasing request times.
  - **Recommendation**: Transition DAO methods to use async counterparts (`await db.SaveChangesAsync()`, `await db.Sanphams.FindAsync()`).

---

## 3. Caching Strategies
- **Token Cache**: `FaceRentalTokenService` utilizes `HttpRuntime.Cache` to save verification records with a short expiration timeout.
- **Uncached Master Data**: Static master lists (e.g. `StoreLocations` and `Category`) are loaded from the database on every query.
  - **Recommendation**: Cache `StoreLocation` details in memory since store addresses and coordinates change infrequently. This will avoid database roundtrips for geofence validation.

---

## 4. Resource Allocation & File Handling
- **Disk I/O Overhead**: Image files received during CMND OCR uploads are saved to disk, read back to open an HTTP stream, and then sent to the Python Flask API.
- **Optimizations**: Read incoming files directly into memory streams and pass them to the HTTP multipart content buffer, bypassing disk writes for temporary files.
