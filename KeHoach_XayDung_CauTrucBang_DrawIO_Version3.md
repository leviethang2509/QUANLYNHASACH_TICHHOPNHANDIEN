# Ke hoach xay dung cau truc bang bang draw.io cho BaoCaoMauSua_Version3

## 1. Muc tieu

- Dung lai toan bo nhom hinh Chuong 3 trong `BaoCaoMauSua_Version3.docx`.
- Moi hinh phai co file nguon `.drawio` rieng de sau nay co the mo bang diagrams.net/draw.io va sua tiep.
- Anh chen vao Word phai la PNG duoc xuat/chup lai tu chinh layout `.drawio`, tuong tu cach da lam voi nhom use case trong `use_case_drawio`.
- Sau khi sinh anh PNG, thay truc tiep cac media tu `word/media/image14.png` den `word/media/image39.png` trong `BaoCaoMauSua_Version3.docx`.
- Neu khong chup truc tiep duoc tu SQL Server, ve bang va quan he bang draw.io dua tren source: `Mood\EF2`, `sql\create_database.sql`, `sql\migrations`, controller/service lien quan.

## 2. Nguyen tac thuc hien giong use case

| Noi dung | Use case da lam | Database Version3 can lam |
|---|---|---|
| Thu muc file nguon | `use_case_drawio` | `database_drawio` |
| Thu muc anh xuat | `use_case_drawio_exports` | `database_drawio_exports` |
| File co the sua sau | `.drawio` import duoc len diagrams.net | `.drawio` import duoc len diagrams.net |
| Anh chen Word | PNG xuat tu `.drawio` | PNG xuat/chup tu `.drawio` |
| Cap nhat Word | Thay media trong DOCX | Thay `image14.png` den `image39.png` |
| Ghi lich su | `LichSuXayDungHinhUseCase.md` | `LichSuXayDungHinhDatabase.md` |

Quy trinh bat buoc:

1. Tao/cap nhat file `.drawio`.
2. Mo/xuat/chup lai anh PNG tu file `.drawio`.
3. Dung PNG do de chen vao `BaoCaoMauSua_Version3.docx`.
4. Giu lai ca `.drawio` va PNG export de lan sau sua khong phai ve lai tu dau.

## 3. Pham vi hinh can thay trong Word

| So hinh | Media trong Word | File draw.io du kien | File PNG export du kien | Noi dung can dung |
|---|---|---|---|---|
| Hinh 3-1 | `word/media/image14.png` | `database_drawio/hinh_3_01_cau_truc_database_cua_du_an_sau_khi_thiet_ke.drawio` | `database_drawio_exports/hinh_3_01_cau_truc_database_cua_du_an_sau_khi_thiet_ke.png` | Cau truc database sau khi thiet ke |
| Hinh 3-2 | `word/media/image15.png` | `database_drawio/hinh_3_02_chi_tiet_bang_users.drawio` | `database_drawio_exports/hinh_3_02_chi_tiet_bang_users.png` | Chi tiet bang Users |
| Hinh 3-3 | `word/media/image16.png` | `database_drawio/hinh_3_03_chi_tiet_bang_rentalrequests.drawio` | `database_drawio_exports/hinh_3_03_chi_tiet_bang_rentalrequests.png` | Chi tiet bang RentalRequests |
| Hinh 3-4 | `word/media/image17.png` | `database_drawio/hinh_3_04_chi_tiet_bang_slides.drawio` | `database_drawio_exports/hinh_3_04_chi_tiet_bang_slides.png` | Chi tiet bang Slides |
| Hinh 3-5 | `word/media/image18.png` | `database_drawio/hinh_3_05_chi_tiet_bang_storelocations.drawio` | `database_drawio_exports/hinh_3_05_chi_tiet_bang_storelocations.png` | Chi tiet bang StoreLocations |
| Hinh 3-6 | `word/media/image19.png` | `database_drawio/hinh_3_06_chi_tiet_bang_categories.drawio` | `database_drawio_exports/hinh_3_06_chi_tiet_bang_categories.png` | Chi tiet bang Categories |
| Hinh 3-7 | `word/media/image20.png` | `database_drawio/hinh_3_07_chi_tiet_bang_productfavorites.drawio` | `database_drawio_exports/hinh_3_07_chi_tiet_bang_productfavorites.png` | Chi tiet bang ProductFavorites |
| Hinh 3-8 | `word/media/image21.png` | `database_drawio/hinh_3_08_chi_tiet_bang_productreviews.drawio` | `database_drawio_exports/hinh_3_08_chi_tiet_bang_productreviews.png` | Chi tiet bang ProductReviews |
| Hinh 3-9 | `word/media/image22.png` | `database_drawio/hinh_3_09_chi_tiet_bang_users__ho_so_dinh_danh.drawio` | `database_drawio_exports/hinh_3_09_chi_tiet_bang_users__ho_so_dinh_danh.png` | Users, phan ho so dinh danh |
| Hinh 3-10 | `word/media/image23.png` | `database_drawio/hinh_3_10_chi_tiet_bang_faceauthlogs.drawio` | `database_drawio_exports/hinh_3_10_chi_tiet_bang_faceauthlogs.png` | Chi tiet bang FaceAuthLogs |
| Hinh 3-11 | `word/media/image24.png` | `database_drawio/hinh_3_11_chi_tiet_bang_productfavorites__quan_he_user_va_sach.drawio` | `database_drawio_exports/hinh_3_11_chi_tiet_bang_productfavorites__quan_he_user_va_sach.png` | ProductFavorites, quan he User - Sach |
| Hinh 3-12 | `word/media/image25.png` | `database_drawio/hinh_3_12_chi_tiet_bang_facesamples.drawio` | `database_drawio_exports/hinh_3_12_chi_tiet_bang_facesamples.png` | FaceSamples/face profile luu ngoai DB |
| Hinh 3-13 | `word/media/image26.png` | `database_drawio/hinh_3_13_chi_tiet_bang_orders.drawio` | `database_drawio_exports/hinh_3_13_chi_tiet_bang_orders.png` | Chi tiet bang Orders |
| Hinh 3-14 | `word/media/image27.png` | `database_drawio/hinh_3_14_chi_tiet_bang_orderdetails.drawio` | `database_drawio_exports/hinh_3_14_chi_tiet_bang_orderdetails.png` | Chi tiet bang OrderDetails |
| Hinh 3-15 | `word/media/image28.png` | `database_drawio/hinh_3_15_chi_tiet_bang_sanphams.drawio` | `database_drawio_exports/hinh_3_15_chi_tiet_bang_sanphams.png` | Chi tiet bang Sanphams |
| Hinh 3-16 | `word/media/image29.png` | `database_drawio/hinh_3_16_chi_tiet_bang_users__tai_khoan_va_phan_quyen.drawio` | `database_drawio_exports/hinh_3_16_chi_tiet_bang_users__tai_khoan_va_phan_quyen.png` | Users, tai khoan va phan quyen |
| Hinh 3-17 | `word/media/image30.png` | `database_drawio/hinh_3_17_chi_tiet_bang_faceauthlogs__vong_doi_xac_thuc.drawio` | `database_drawio_exports/hinh_3_17_chi_tiet_bang_faceauthlogs__vong_doi_xac_thuc.png` | FaceAuthLogs, vong doi xac thuc |
| Hinh 3-18 | `word/media/image31.png` | `database_drawio/hinh_3_18_chi_tiet_bang_quyens.drawio` | `database_drawio_exports/hinh_3_18_chi_tiet_bang_quyens.png` | Chi tiet bang Quyens |
| Hinh 3-19 | `word/media/image32.png` | `database_drawio/hinh_3_19_chi_tiet_bang_rentallogs.drawio` | `database_drawio_exports/hinh_3_19_chi_tiet_bang_rentallogs.png` | Chi tiet bang RentalLogs |
| Hinh 3-20 | `word/media/image33.png` | `database_drawio/hinh_3_20_chi_tiet_bang_userquyens.drawio` | `database_drawio_exports/hinh_3_20_chi_tiet_bang_userquyens.png` | UserQuyens/quan he User - Quyen |
| Hinh 3-21 | `word/media/image34.png` | `database_drawio/hinh_3_21_chi_tiet_bang_facerentaltokens.drawio` | `database_drawio_exports/hinh_3_21_chi_tiet_bang_facerentaltokens.png` | FaceRentalTokens, cau truc logic token |
| Hinh 3-22 | `word/media/image35.png` | `database_drawio/hinh_3_22_chi_tiet_bang_facerentaltokens__vong_doi_token.drawio` | `database_drawio_exports/hinh_3_22_chi_tiet_bang_facerentaltokens__vong_doi_token.png` | FaceRentalTokens, vong doi token |
| Hinh 3-23 | `word/media/image36.png` | `database_drawio/hinh_3_23_chi_tiet_bang_storelocations__geofence.drawio` | `database_drawio_exports/hinh_3_23_chi_tiet_bang_storelocations__geofence.png` | StoreLocations va quan he GeofenceLogs |
| Hinh 3-24 | `word/media/image37.png` | `database_drawio/hinh_3_24_chi_tiet_bang_rentallogs__trang_thai_muon_tra.drawio` | `database_drawio_exports/hinh_3_24_chi_tiet_bang_rentallogs__trang_thai_muon_tra.png` | RentalLogs theo trang thai muon/tra |
| Hinh 3-25 | `word/media/image38.png` | `database_drawio/hinh_3_25_chi_tiet_bang_geofencelogs.drawio` | `database_drawio_exports/hinh_3_25_chi_tiet_bang_geofencelogs.png` | Chi tiet bang GeofenceLogs |
| Hinh 3-26 | `word/media/image39.png` | `database_drawio/hinh_3_26_cau_truc_database_cua_du_an_sau_khi_da_cai_dat.drawio` | `database_drawio_exports/hinh_3_26_cau_truc_database_cua_du_an_sau_khi_da_cai_dat.png` | Cau truc database sau khi da cai dat |

## 4. Nguon doi chieu

| Nhom | File doi chieu |
|---|---|
| Entity Framework model | `Mood\EF2\*.cs` |
| DbContext chinh | `Mood\EF2\QuanLySachDBContext.cs` |
| DbContext log | `Mood\EF2\LogDbContext.cs` |
| Script tao database | `sql\create_database.sql` |
| Migration chuc nang moi | `sql\migrations\*.sql` |
| Luong muon/tra sach | `BaiTapLon\Controllers\RentalController.cs`, `BaiTapLon\Services\GmailNotificationService.cs` |
| Luong xac thuc khuon mat | `BaiTapLon\Controllers\FaceAuthController.cs`, `BaiTapLon\Services\FaceAuthApiClient.cs`, `face_auth_api\app.py` |
| Token muon sach | `BaiTapLon\Services\FaceRentalTokenService.cs`, `BaiTapLon\Web.config` |
| Log/geofence | `Common\Repositories\LogRepository.cs`, `BaiTapLon\Controllers\GeofenceController.cs` |

## 5. Quy tac trinh bay trong draw.io

- File `.drawio` phai dung shape bang ro rang: header nen xanh nhat, body nen trang, vien xam/den de khi chen vao Word van doc duoc.
- Truong khoa chinh ghi `PK`, khoa ngoai ghi `FK`, cac rang buoc quan trong ghi `UNIQUE`, `INDEX`, `NOT NULL` neu can.
- Hinh tong quan `Hinh 3-1` va `Hinh 3-26` ve dang ERD nhieu bang, co duong quan he giua cac bang chinh.
- Hinh chi tiet ve mot bang chinh, co them ghi chu nguon model/migration o goc duoi.
- Cac cau truc khong ton tai vat ly trong SQL Server nhu `FaceSamples`, `FaceRentalTokens`, `UserQuyens` neu chi la logic thi phai ghi ro: `Cau truc logic / luu ngoai DB`.
- Ten cot va ten bang uu tien lay tu source thuc te, khong tu y doi ten cho dep neu source dang dung ten khac.
- PNG export phai du lon, nen toi thieu 1600px chieu ngang voi hinh tong quan va 1000px voi hinh chi tiet bang.

## 6. Thu tu thuc hien

| Buoc | Cong viec | Ket qua |
|---|---|---|
| 1 | Kiem tra source database/model/migration va mapping media trong Word | Biet dung bang, cot, quan he va anh can thay |
| 2 | Tao/cap nhat thu muc `database_drawio` | Noi luu file nguon `.drawio` de sua ve sau |
| 3 | Sinh 26 file `.drawio` theo mapping Hinh 3-1 den Hinh 3-26 | Import duoc vao diagrams.net/draw.io |
| 4 | Xuat/chup lai 26 PNG tu chinh cac file `.drawio` | Anh moi nam trong `database_drawio_exports` |
| 5 | Backup `BaoCaoMauSua_Version3.docx` | Co file phuc hoi, vi du `BaoCaoMauSua_Version3.before_database_update.docx` |
| 6 | Thay `word/media/image14.png` den `word/media/image39.png` bang PNG moi | Chuong 3 trong Word dung anh moi |
| 7 | Luu DOCX cap nhat, neu file goc bi khoa thi tao file fallback | Vi du `BaoCaoMauSua_Version3_DatabaseDrawIO.docx` |
| 8 | Kiem tra DOCX la zip hop le va co du media moi | Dam bao file Word khong hong |
| 9 | Ghi ket qua vao `LichSuXayDungHinhDatabase.md` | Co nhat ky file draw.io, PNG export va media da thay |

## 7. Cach cap nhat vao BaoCaoMauSua_Version3.docx

- Mo DOCX nhu mot file zip tam.
- Thay dung cac file trong `word/media` theo mapping o muc 3.
- Khong doi ten media trong Word neu khong can, de giu nguyen lien ket anh/caption/danh muc hinh.
- Sau khi dong zip lai, kiem tra:
  - File `.docx` mo duoc bang Word.
  - Hinh 3-1 den Hinh 3-26 hien anh moi.
  - Anh khong bi mo, cat mat, hoac sai ty le.
  - Danh muc hinh van giu dung so hinh.

## 8. Checklist nghiem thu

- Co du 26 file `.drawio` trong `database_drawio`.
- Co du 26 file PNG trong `database_drawio_exports`.
- Moi PNG duoc xuat/chup lai tu file `.drawio` tuong ung.
- `BaoCaoMauSua_Version3.docx` da duoc backup truoc khi thay anh.
- `word/media/image14.png` den `word/media/image39.png` da duoc thay dung thu tu.
- Hinh logic/luu ngoai DB da ghi chu ro, tranh nham la bang vat ly.
- `LichSuXayDungHinhDatabase.md` co ghi ro ngay gio, file source, file export va ket qua cap nhat Word.

## 9. Script nen dung

Script chinh can dung/cap nhat:

- `scripts\generate_database_drawio_and_update_version3.py`

Script nay nen dam nhan tron luong:

1. Doc cau hinh 26 hinh database.
2. Sinh file `.drawio` vao `database_drawio`.
3. Xuat/chup PNG vao `database_drawio_exports`.
4. Backup `BaoCaoMauSua_Version3.docx`.
5. Thay media trong DOCX.
6. Kiem tra DOCX sau khi ghi.
7. Ghi lich su vao `LichSuXayDungHinhDatabase.md`.

## 10. Ghi chu sua ve sau

- Khi can sua mot hinh, sua file `.drawio` trong `database_drawio`, sau do xuat lai PNG cung ten vao `database_drawio_exports`.
- Neu chi sua mot hinh, chi can thay lai media Word tuong ung theo bang mapping, khong can sinh lai tat ca.
- Khong sua truc tiep PNG bang cong cu ve anh neu thay doi lien quan den noi dung so do; nguon chinh van phai la `.drawio`.
